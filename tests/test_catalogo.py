def test_categoria_duplicada_retorna_409(client):
    assert client.post("/categorias", json={"nome": "Bebidas"}).status_code == 201
    assert client.post("/categorias", json={"nome": "Bebidas"}).status_code == 409


def test_nao_apaga_categoria_com_produtos(client, criar_produto):
    produto = criar_produto()
    resp = client.delete(f"/categorias/{produto['categoria_id']}")
    assert resp.status_code == 409


def test_nao_apaga_produto_ja_vendido(client, criar_produto):
    produto = criar_produto()
    client.post("/vendas", json={"itens": [{"produto_id": produto["id"], "quantidade": 1}]})
    assert client.delete(f"/produtos/{produto['id']}").status_code == 409
