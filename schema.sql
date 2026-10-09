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