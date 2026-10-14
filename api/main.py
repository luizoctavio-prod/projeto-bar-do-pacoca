from decimal import Decimal
from api.schemas import (Categoria, CategoriaCreate, Produto, ProdutoCreate,
                         Venda, VendaCreate)

from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2 import errors

from api.database import get_db
from api.schemas import Categoria, CategoriaCreate, Produto, ProdutoCreate

app = FastAPI(
    title="API - Bar do Paçoca",
    description="Controle de categorias e produtos do estabelecimento.",
    version="0.1.0",
)

COLUNAS_PRODUTO = "id, nome, categoria_id, preco, estoque"


# ---------- Categorias ----------

@app.get("/categorias", response_model=list[Categoria], tags=["Categorias"])
def listar_categorias(db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT id, nome FROM categorias ORDER BY nome;")
        return cur.fetchall()


@app.post("/categorias", response_model=Categoria,
          status_code=status.HTTP_201_CREATED, tags=["Categorias"])
def criar_categoria(dados: CategoriaCreate, db=Depends(get_db)):
    try:
        with db.cursor() as cur:
            cur.execute(
                "INSERT INTO categorias (nome) VALUES (%s) RETURNING id, nome;",
                (dados.nome,),
            )
            categoria = cur.fetchone()
        db.commit()
        return categoria
    except errors.UniqueViolation:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "Já existe uma categoria com esse nome.")


@app.delete("/categorias/{categoria_id}",
            status_code=status.HTTP_204_NO_CONTENT, tags=["Categorias"])
def excluir_categoria(categoria_id: int, db=Depends(get_db)):
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM categorias WHERE id = %s;", (categoria_id,))
            if cur.rowcount == 0:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    "Categoria não encontrada.")
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except errors.ForeignKeyViolation:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "A categoria ainda possui produtos.")


# ---------- Produtos ----------

@app.get("/produtos", response_model=list[Produto], tags=["Produtos"])
def listar_produtos(categoria_id: int | None = None,
                    busca: str | None = None,
                    db=Depends(get_db)):
    sql = f"SELECT {COLUNAS_PRODUTO} FROM produtos WHERE TRUE"
    params = []
    if categoria_id is not None:
        sql += " AND categoria_id = %s"
        params.append(categoria_id)
    if busca:
        sql += " AND nome ILIKE %s"
        params.append(f"%{busca}%")
    sql += " ORDER BY id;"
    with db.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


@app.get("/produtos/{produto_id}", response_model=Produto, tags=["Produtos"])
def obter_produto(produto_id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(f"SELECT {COLUNAS_PRODUTO} FROM produtos WHERE id = %s;",
                    (produto_id,))
        produto = cur.fetchone()
    if produto is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado.")
    return produto


@app.post("/produtos", response_model=Produto,
          status_code=status.HTTP_201_CREATED, tags=["Produtos"])
def criar_produto(dados: ProdutoCreate, db=Depends(get_db)):
    try:
        with db.cursor() as cur:
            cur.execute(
                f"""INSERT INTO produtos (nome, categoria_id, preco, estoque)
                    VALUES (%s, %s, %s, %s) RETURNING {COLUNAS_PRODUTO};""",
                (dados.nome, dados.categoria_id, dados.preco, dados.estoque),
            )
            produto = cur.fetchone()
        db.commit()
        return produto
    except errors.UniqueViolation:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "Já existe esse produto nessa categoria.")
    except errors.ForeignKeyViolation:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "A categoria informada não existe.")


@app.put("/produtos/{produto_id}", response_model=Produto, tags=["Produtos"])
def atualizar_produto(produto_id: int, dados: ProdutoCreate,
                      db=Depends(get_db)):
    try:
        with db.cursor() as cur:
            cur.execute(
                f"""UPDATE produtos
                    SET nome = %s, categoria_id = %s, preco = %s, estoque = %s
                    WHERE id = %s RETURNING {COLUNAS_PRODUTO};""",
                (dados.nome, dados.categoria_id, dados.preco, dados.estoque,
                 produto_id),
            )
            produto = cur.fetchone()
        if produto is None:
            db.rollback()
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                "Produto não encontrado.")
        db.commit()
        return produto
    except errors.UniqueViolation:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "Já existe esse produto nessa categoria.")
    except errors.ForeignKeyViolation:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "A categoria informada não existe.")


@app.delete("/produtos/{produto_id}",
            status_code=status.HTTP_204_NO_CONTENT, tags=["Produtos"])
def excluir_produto(produto_id: int, db=Depends(get_db)):
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM produtos WHERE id = %s;", (produto_id,))
            if cur.rowcount == 0:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    "Produto não encontrado.")
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except errors.ForeignKeyViolation:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "O produto já tem vendas e não pode ser removido.")

# ---------- Vendas ---------- #

@app.post("/vendas", response_model=Venda,
          status_code=status.HTTP_201_CREATED, tags=["Vendas"])
def registrar_venda(dados: VendaCreate, db=Depends(get_db)):
    # Junta linhas repetidas do mesmo produto em uma só
    quantidades: dict[int, int] = {}
    for item in dados.itens:
        quantidades[item.produto_id] = (
            quantidades.get(item.produto_id, 0) + item.quantidade
        )

    try:
        with db.cursor() as cur:
            itens = []
            total = Decimal("0")

            # Em ordem de id, para evitar travamento entre vendas simultâneas
            for produto_id in sorted(quantidades):
                quantidade = quantidades[produto_id]
                # FOR UPDATE trava a linha até o fim da transação
                cur.execute(
                    "SELECT nome, preco, estoque FROM produtos "
                    "WHERE id = %s FOR UPDATE;",
                    (produto_id,),
                )
                produto = cur.fetchone()
                if produto is None:
                    raise HTTPException(status.HTTP_404_NOT_FOUND,
                                        f"Produto {produto_id} não encontrado.")
                if produto["estoque"] < quantidade:
                    raise HTTPException(
                        status.HTTP_409_CONFLICT,
                        f"Estoque insuficiente para '{produto['nome']}' "
                        f"(disponível: {produto['estoque']}).",
                    )
                itens.append({"produto_id": produto_id,
                              "quantidade": quantidade,
                              "preco_unitario": produto["preco"]})
                total += produto["preco"] * quantidade

            cur.execute(
                "INSERT INTO vendas (total) VALUES (%s) "
                "RETURNING id, data_hora, total;",
                (total,),
            )
            venda = cur.fetchone()

            for item in itens:
                cur.execute(
                    "INSERT INTO itens_venda "
                    "(venda_id, produto_id, quantidade, preco_unitario) "
                    "VALUES (%s, %s, %s, %s);",
                    (venda["id"], item["produto_id"], item["quantidade"],
                     item["preco_unitario"]),
                )
                cur.execute(
                    "UPDATE produtos SET estoque = estoque - %s WHERE id = %s;",
                    (item["quantidade"], item["produto_id"]),
                )
        db.commit()
        return {**venda, "itens": itens}
    except Exception:
        db.rollback()
        raise


@app.get("/vendas/{venda_id}", response_model=Venda, tags=["Vendas"])
def obter_venda(venda_id: int, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT id, data_hora, total FROM vendas WHERE id = %s;",
                    (venda_id,))
        venda = cur.fetchone()
        if venda is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                "Venda não encontrada.")
        cur.execute(
            "SELECT produto_id, quantidade, preco_unitario "
            "FROM itens_venda WHERE venda_id = %s ORDER BY id;",
            (venda_id,),
        )
        itens = cur.fetchall()
    return {**venda, "itens": itens}

