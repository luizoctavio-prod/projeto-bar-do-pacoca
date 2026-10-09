import psycopg2

DB_NAME = 'mercearia_db'
DB_USER = 'postgres'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '5432'

try:
    conexao = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conexao.cursor()

    carrinho = []

    while True:
        id_produto = int(input('Digite o ID do produto: '))
        quantidade = int(input('Digite a quantidade: '))
        carrinho.append((id_produto, quantidade))

        continuar = input("Deseja adicionar mais um produto? (s/n): ")
        if continuar.lower() == 'n':
            break

    total_venda = 0.0

    print("\n--- Processando Carrinho ---")
    for id_prod, qtd in carrinho:
        cursor.execute("SELECT preco, estoque FROM produtos WHERE id = %s;", (id_prod,))
        produto = cursor.fetchone()

        if not produto:
            raise Exception(f"Produto ID {id_prod} não foi encontrado no sistema!")

        preco_unitario = produto[0]
        estoque_atual = produto[1]


        if qtd > estoque_atual:
            raise Exception(f"Estoque insuficiente para o produto ID {id_prod}! Disponível: {estoque_atual}")


        total_venda += float(preco_unitario) * qtd


        cursor.execute('''
            UPDATE produtos 
            SET estoque = estoque - %s 
            WHERE id = %s;
        ''', (qtd, id_prod))


    print(f"\n VENDA CONCLUÍDA COM SUCESSO!")
    print(f"Total a Pagar: R$ {total_venda:.2f}")

    conexao.commit()

except Exception as erro:
    
    if 'conexao' in locals() and conexao:
        conexao.rollback()
    print(f'Ocorreu um erro ao processar a venda: {erro}')

finally:
    if 'conexao' in locals() and conexao:
        cursor.close()
        conexao.close()
        print('Conexao encerrada com sucesso!')
