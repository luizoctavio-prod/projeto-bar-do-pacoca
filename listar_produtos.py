import psycopg2

# Configurações de acesso ao banco de dados
DB_USER = 'postgres'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_NAME = 'mercearia_db'
DB_PORT = '5432'

try:
    # 1. Abre a conexão e o cursor com o banco de dados
    conexao = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conexao.cursor()

    # 2. Executa a busca cruzando as duas tabelas com INNER JOIN
    cursor.execute('''
        SELECT produtos.id, produtos.nome, categorias.nome, produtos.preco, produtos.estoque
        FROM produtos
        INNER JOIN categorias ON produtos.categoria_id = categorias.id;
    ''')

    # 3. Puxa os dados para o Python
    todos_os_produtos = cursor.fetchall()

    # 4. Exibe os dados organizados linha por linha no terminal
    print("\n--- RELATÓRIO DE PRODUTOS DA MERCEARIA ---")
    for id_prod, nome_prod, nome_cat, prod_preco, prod_est in todos_os_produtos:
        print(f"ID: {id_prod} | Produto: {nome_prod} | Categoria: {nome_cat} | Preco: {prod_preco} | Estoque: {prod_est}")
    print("------------------------------------------\n")

except Exception as erro:
    # Captura e exibe qualquer erro caso algo falhe
    print(f"Ocorreu um erro ao listar os produtos: {erro}")

finally:
    # Garante o fechamento seguro do cursor e da conexão
    if 'conexao' in locals() and conexao:
        cursor.close()
        conexao.close()
        print("Conexão com o banco de dados fechada.")