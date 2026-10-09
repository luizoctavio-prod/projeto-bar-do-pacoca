import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from categorias import cursor

# 1. Configurações de acesso ao seu PostgreSQL
# ADICIONE A SUA SENHA DO POSTGRES ABAIXO
DB_USER = "postgres"
DB_PASSWORD = "SUA_SENHA_AQUI"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mercearia_db"


def inicializar_sistema():
    # Conecta ao banco padrão 'postgres' para poder criar o novo banco
    conexao_inicial = psycopg2.connect(
        user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database="postgres"
    )
    conexao_inicial.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor_inicial = conexao_inicial.cursor()

    # Cria o banco de dados da mercearia
    try:
        cursor_inicial.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Banco de dados '{DB_NAME}' criado com sucesso!")
    except psycopg2.errors.DuplicateDatabase:
        print(f"O banco de dados '{DB_NAME}' já existe. Prosseguindo...")
    finally:
        cursor_inicial.close()
        conexao_inicial.close()

    # 2. Conecta especificamente no novo banco para criar as tabelas
    conexao_mercearia = psycopg2.connect(
        user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, database=DB_NAME
    )
    cursor = conexao_mercearia.cursor()

    # SQL para gerar as tabelas
    script_tabelas = """
    CREATE TABLE IF NOT EXISTS categorias (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS produtos (
        id SERIAL PRIMARY KEY,
        codigo_barras VARCHAR(50) UNIQUE,
        nome VARCHAR(150) NOT NULL,
        preco_venda NUMERIC(10, 2) NOT NULL,
        estoque_atual INT NOT NULL DEFAULT 0,
        categoria_id INT REFERENCES categorias(id) ON DELETE SET NULL
    );
    """

    try:
        cursor.execute(script_tabelas)
        conexao_mercearia.commit()
        print("Tabelas 'categorias' e 'produtos' criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        conexao_mercearia.rollback()
    finally:
        cursor.close()
        conexao_mercearia.close()


if __name__ == "__main__":
    inicializar_sistema()

