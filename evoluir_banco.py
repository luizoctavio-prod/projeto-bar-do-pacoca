

import psycopg2


DB_USER = 'postgres'
DB_HOST = 'localhost'
DB_NAME = 'mercearia_db'
DB_PASSWORD = ''
DB_PORT = '5432'


try:
    conexao = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        password=DB_PASSWORD,
        user=DB_USER,
        port=DB_PORT,
    )
    cursor = conexao.cursor()

    cursor.execute('''
    ALTER TABLE produtos ADD COLUMN preco DECIMAL(10, 2) DEFAULT 0.00;
    ALTER TABLE produtos ADD COLUMN estoque INTEGER DEFAULT 0;''')

    conexao.commit()
    print('Banco de Dados evoluído!! Novas Colunas adicionadas com sucesso!')

except Exception as erro:
    print(f'Ocorreu um erro ao alterar a tabela: {erro}')

finally:
    if 'conexao' in locals() and conexao:
        cursor.close()
        conexao.close()
        print('Conexão com o Banco de Dados fechada com sucesso!')
        

