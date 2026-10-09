import psycopg2

DB_NAME = 'mercearia_db'
DB_USER = 'postgres'
DB_PASSWORD = ''
DB_HOST =  'localhost'
DB_PORT = '5432'


try:
    conexao = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

    cursor = conexao.cursor()

    while True:
        id_desejado = int(input('Digite o ID do produto que quer atualizar: '))
        novo_preco = float(input('Digite o Novo Preço do produto: '))
        novo_estoque = int(input('Digite a Nova quantidade em estoque: '))

        cursor.execute('''
        UPDATE produtos
        SET preco = %s, estoque = %s
        where id = %s
        ''',(novo_preco, novo_estoque, id_desejado))

        conexao.commit()
        print('Nova Tabela atualizada com sucesso!')

        continuar = input("Deseja atualizar outro produto? (s/n): ")

        if continuar.lower() == 'n':
            break


except Exception as erro:
    print(f'Ocorreu um erro ao alterar a tabela de produtos: {erro}')


finally:
    if 'conexao' in locals() and conexao:
        cursor.close()
        conexao.close()
        print('Conexao com o Banco de Dados fchada com sucesso!')
