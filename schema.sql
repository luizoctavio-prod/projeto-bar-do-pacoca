CREATE TABLE categorias (
    id   SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE produtos (
    id           SERIAL PRIMARY KEY,
    nome         VARCHAR(150) NOT NULL,
    categoria_id INTEGER NOT NULL
                 REFERENCES categorias(id) ON DELETE RESTRICT,
    preco        NUMERIC(10,2) NOT NULL DEFAULT 0.00
                 CHECK (preco >= 0),
    estoque      INTEGER NOT NULL DEFAULT 0
                 CHECK (estoque >= 0),
    CONSTRAINT produto_unico UNIQUE (nome, categoria_id)
);

CREATE TABLE vendas (
    id        SERIAL PRIMARY KEY,
    data_hora TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total     NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (total >= 0)
);

CREATE TABLE itens_venda (
    id             SERIAL PRIMARY KEY,
    venda_id       INTEGER NOT NULL REFERENCES vendas(id) ON DELETE CASCADE,
    produto_id     INTEGER NOT NULL REFERENCES produtos(id) ON DELETE RESTRICT,
    quantidade     INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(10,2) NOT NULL CHECK (preco_unitario >= 0)
);

CREATE INDEX idx_vendas_data ON vendas (data_hora);
CREATE INDEX idx_itens_venda_venda ON itens_venda (venda_id);
CREATE INDEX idx_itens_venda_produto ON itens_venda (produto_id);