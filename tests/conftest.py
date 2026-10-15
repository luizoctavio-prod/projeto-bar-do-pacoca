import os
from pathlib import Path

import psycopg2
import pytest
from dotenv import load_dotenv

load_dotenv()

TEST_DB = "mercearia_test"
# Os testes NUNCA usam o banco real: força o banco de teste antes de importar a API
os.environ["DB_NAME"] = TEST_DB

from fastapi.testclient import TestClient  # noqa: E402

from api.main import app  # noqa: E402


def _conectar(dbname):
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        dbname=dbname,
    )


@pytest.fixture(scope="session", autouse=True)
def banco_de_teste():
    """Cria o banco de teste (se não existir) e recria as tabelas do schema.sql."""
    admin = _conectar("postgres")
    admin.autocommit = True
    with admin.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (TEST_DB,))
        if cur.fetchone() is None:
            cur.execute(f"CREATE DATABASE {TEST_DB};")
    admin.close()

    schema = (Path(__file__).resolve().parent.parent / "schema.sql").read_text(
        encoding="utf-8"
    )
    conn = _conectar(TEST_DB)
    with conn.cursor() as cur:
        cur.execute(
            "DROP TABLE IF EXISTS itens_venda, vendas, produtos, categorias CASCADE;"
        )
        cur.execute(schema)
    conn.commit()
    conn.close()


@pytest.fixture(autouse=True)
def limpar_tabelas():
    """Cada teste começa com as tabelas vazias."""
    conn = _conectar(TEST_DB)
    with conn.cursor() as cur:
        cur.execute(
            "TRUNCATE itens_venda, vendas, produtos, categorias "
            "RESTART IDENTITY CASCADE;"
        )
    conn.commit()
    conn.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def criar_produto(client):
    categoria = client.post("/categorias", json={"nome": "Bebidas"}).json()

    def _criar(nome="Cerveja", preco="5.50", estoque=10):
        resp = client.post(
            "/produtos",
            json={"nome": nome, "categoria_id": categoria["id"],
                  "preco": preco, "estoque": estoque},
        )
        assert resp.status_code == 201
        return resp.json()

    return _criar