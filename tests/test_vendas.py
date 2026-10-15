def vender(client, *itens):
    return client.post(
        "/vendas",
        json={"itens": [{"produto_id": p, "quantidade": q} for p, q in itens]},
    )


def estoque_de(client, produto_id):
    return client.get(f"/produtos/{produto_id}").json()["estoque"]


def test_venda_com_sucesso_baixa_estoque(client, criar_produto):
    produto = criar_produto(preco="5.50", estoque=10)

    resp = vender(client, (produto["id"], 2))

    assert resp.status_code == 201
    assert resp.json()["total"] == "11.00"
    assert estoque_de(client, produto["id"]) == 8


def test_estoque_insuficiente_retorna_409_e_nao_altera_estoque(client, criar_produto):
    produto = criar_produto(estoque=10)

    resp = vender(client, (produto["id"], 11))

    assert resp.status_code == 409
    assert estoque_de(client, produto["id"]) == 10


def test_produto_inexistente_retorna_404(client):
    assert vender(client, (999999, 1)).status_code == 404


def test_quantidade_zero_retorna_422(client, criar_produto):
    produto = criar_produto()
    assert vender(client, (produto["id"], 0)).status_code == 422


def test_venda_e_tudo_ou_nada(client, criar_produto):
    produto = criar_produto(estoque=10)

    # O segundo item não existe: a venda inteira deve ser desfeita
    resp = vender(client, (produto["id"], 1), (999999, 1))

    assert resp.status_code == 404
    assert estoque_de(client, produto["id"]) == 10


def test_faturamento_diario_soma_as_vendas(client, criar_produto):
    produto = criar_produto(preco="5.50", estoque=20)
    vender(client, (produto["id"], 2))
    vender(client, (produto["id"], 3))

    dias = client.get("/relatorios/faturamento-diario?dias=1").json()

    assert len(dias) == 1
    assert dias[0]["vendas"] == 2
    assert dias[0]["faturamento"] == "27.50"


def test_mais_vendidos_ordena_por_quantidade(client, criar_produto):
    a = criar_produto(nome="Agua", preco="3.00", estoque=50)
    b = criar_produto(nome="Cerveja", preco="10.00", estoque=50)
    vender(client, (a["id"], 5), (b["id"], 2))

    ranking = client.get("/relatorios/mais-vendidos?dias=1").json()

    assert [p["nome"] for p in ranking] == ["Agua", "Cerveja"]
    assert ranking[0]["quantidade_vendida"] == 5