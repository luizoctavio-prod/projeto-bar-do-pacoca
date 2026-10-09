import psycopg2
from tabulate import tabulate

DB_NAME = 'mercearia_db'
DB_USER = 'postgres'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '5432'

try:
    # Abre a conexão com o banco de dados da mercearia
    conexao = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conexao.cursor()

    # 1. Executa a busca trazendo as colunas ordenadas por ID
    cursor.execute("SELECT id, nome, preco, estoque FROM produtos ORDER BY id;")
    dados = cursor.fetchall()

    # 2. Define os cabeçalhos das colunas exatamente na ordem do SELECT
    colunas = ["ID", "Nome do Produto", "Preço", "Estoque Atual"]

    # 3. Desenha e imprime a tabela em formato de grade organizada
    print("\n======================= ESTOQUE DA MERCEARIA =======================")
    print(tabulate(dados, headers=colunas, tablefmt="grid"))
    print("====================================================================\n")

except Exception as erro:
    print(f'Ocorreu um erro ao gerar o relatório: {erro}')

finally:
    # Garante o fechamento seguro da conexão
    if 'conexao' in locals() and conexao:
        cursor.close()
        conexao.close()
        print('Conexao encerrada com sucesso!')