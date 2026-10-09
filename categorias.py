# responsavel por enviar comando para o banco de dados postgre
import psycopg2

# Configurações de acesso ao banco de dados
DB_USER = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'mercearia_db'
DB_PASSWORD = ''

# 1. LISTA DE CATEGORIAS
lista_categorias = [
    'Cervejas', 'Refrigerantes', 'Porções', 'Cigarros', 'Salgados',
    'Salgadinhos', 'Guloseimas', 'Doces', 'Limpeza e Higiene Pessoal',
    'Destilados', 'Frios', 'Bebidas', 'Laticínios', 'Matinais', 'Alimentos',
    'Molhos e Condimentos', 'Conserva', 'Bazar e Utilidades'
]

# 2. DICIONÁRIO DE PRODUTOS ORGANIZADOS POR CATEGORIA
produtos_por_categoria = {
    'Cervejas': [
        'Boa 600mL', 'Boa 1L', 'Boa 300mL', 'Boa lata 350mL', 'Brahma 1L',
        'Brahma 600mL', 'Brahma 300mL', 'Brahma lata 350mL', 'Brahma lata zero álcool',
        'Skol 600mL', 'Skol 300mL', 'Skol lata 350mL', 'Skol lata zero álcool',
        'Amstel 600mL', 'Amstel lata 350mL', 'Heineken 600mL',
        'Heineken long neck 330mL descartável', 'Heineken long neck 330mL retornável',
        'Heineken lata 350mL', 'Heineken lata zero álcool', 'Budweiser 300mL longneck',
        'Budweiser lata 350mL', 'Kaiser latão 473mL', 'Echo Beer latão 473mL',
        'Império lata 350mL', 'Brahma duplo malte 350mL lata'
    ],
    'Refrigerantes': [
        'Coca 2L Retornável', 'Coca 2L Retornável zero', 'Fanta Laranja Retornável 2L',
        'Coca descartável 2L', 'Coca descartável 2L zero', 'Coca 600mL', 'Coca 1L Retornável',
        'Coca lata 350mL', 'Coca lata 350mL zero', 'Coca KS', 'Coca KS zero', 'Coca RGB 200mL',
        'Coca 200mL descartável', 'Coca 200mL descartável zero', 'Fanta laranja KS', 'Sprite KS',
        'Fanta 2L descartável laranja', 'Fanta 600mL laranja', 'Fanta laranja lata 350mL',
        'Fanta laranja descartável 200mL', 'Sprite 2L descartável', 'Sprite 2L descartável zero',
        'Sprite 600mL', 'Sprite 200mL descartável zero', 'Fanta uva 2L descartável',
        'Fanta 600mL uva', 'Fanta uva 350mL lata', 'Fanta uva 200mL descartável',
        'Schweppes 1,5L descartável', 'Schweppes lata 350mL', 'Guaraná Jaboti 2L',
        'Guaraná Jaboti 600mL', 'Guaraná Antarctica 2L', 'Guaraná Antarctica lata 350mL',
        'Guaraná Antarctica 1L retornável', 'Guaraná Antarctica 200mL'
    ],
    'Porções': [
        'Tilápia frita', 'Frango frito', 'Steak frito', 'Torresmo', 'Pé de porco',
        'Dobradinha', 'Calabresa ao molho', 'Frango assado', 'Salgado frito',
        'Salgado assado', 'Bolinho de carne'
    ],
    'Cigarros': [],
    'Salgados': [
        'Enroladinho presunto e queijo (frito)', 'Enroladinho salsicha (frito)', 'Coxinha',
        'Kibe', 'Kibe de ovo', 'Risole de carne', 'Pastel de carne', 'Pastel de queijo',
        'Pastel de pizza', 'Presunto, queijo e tomate (assado)', 'Enroladinho de presunto e queijo (assado)',
        'Esfiha carne', 'Esfiha frango', 'Enroladinho de salsicha (assado)', 'Hambúrguer'
    ],
    'Salgadinhos': [
        'Lays salsa e cebola 62g', 'Lays taco mexicano 62g', 'Lays queijo cream cheese 62g',
        'Lays picanha 62g', 'Doritos Dinamita', 'Doritos Sweet Chili', 'Lays clássica 30g',
        'Lays salsa e cebola 30g', 'Sensações sabor peito de peru', 'Sensações sabor frango grelhado',
        'Ruffles clássica', 'Ruffles cebola', 'Ruffles churrasco', 'Ruffles extra picante',
        'Baconzitos', 'Cebolitos', 'Cheetos Lua', 'Cheetos Onda', 'Cheetos Mix',
        'Fandangos presunto', 'Fandangos queijo', 'Fandangos churrasco', 'Yokitos Queijo',
        'Yokitos Presunto', 'Yokitos Cebola', 'Yokitos Requeijão', 'Yokitos Batata Clássica',
        'Becs+ sabor presunto', 'Becs+ sabor bacon', 'Becs+ sabor cebola', 'Becs+ sabor churrasco'
    ],
    'Guloseimas': [
        'Bala Icekiss cereja', 'Bala Icekiss extra forte', 'Bala Toffee chocolate',
        'Bala de café', 'Bala de iogurte', 'Bala de hortelã macia', 'Bala de hortelã dura',
        'Bala de frutas sortidas'
    ],
    'Doces': [
        'Chocolate Suflair', 'Chocolate Trento', 'Chocolate branco Laka', 'Guarda-chuva chocolate',
        'Batom chocolate', 'Snickers', 'KitKat', 'Pipoca canelinha da roça'
    ],
    'Limpeza e Higiene Pessoal': [
        'Veja', 'Limpa alumínio Triex índigo', 'Limpa alumínio Limpex', 'Limpa pisos Radja 5L',
        'Desinfetante Pinho Bril 500mL', 'Desinfetante Pinho Sol 500mL', 'Limpador Radja',
        'Esponja multiuso', 'Saco de lixo 15L', 'Triex desinfetante', 'Saco de lixo 30L',
        'Saco de lixo 50L', 'Saco de lixo 100L', 'Detergente Ypê neutro', 'Detergente Ypê coco',
        'Detergente Ypê limão', 'Detergente Limpol neutro', 'Detergente Limpol coco',
        'Detergente Limpol limão', 'Detergente Minuano neutro', 'Detergente Radja neutro',
        'Amaciante Ypê intenso ultra', 'Amaciante Ypê aconchego', 'Amaciante Baby Soft aconchego',
        'Amaciante Radja aconchego', 'Sabão em pó Omo', 'Sabão em pó Tixan', 'Sabão em barra Ypê',
        'Água sanitária Candura 1L', 'Água sanitária Candura 2L', 'Palha de aço (Esponja de aço Bom Bril)',
        'Absorvente Pessoal Intimus', 'Pasta de dente Colgate', 'Escova de dente Sorriso',
        'Sabonete Lux Buquê de Jasmim', 'Sabonete Protex', 'Papel Higiênico Personal',
        'Desodorante spray Rexona Active', 'Desodorante spray Rexona WG', 'Condicionador Liso Perfeito Seda',
        'Condicionador Pretos Luminosos Seda', 'Condicionador Cachos Definidos Seda',
        'Shampoo Seda Liso Extremo', 'Triex aromatizante lavanda', 'Triex aromatizante eucalipto citriodora'
    ],
    'Destilados': [
        'Velho Barreiro', 'Jamel', '51', 'Conhaque de mel', 'Conhaque Domus', 'Conhaque Presidente',
        'Whisky Old Eight', 'Paizano', 'Jurubeba', 'Vodka Sky', 'Ypióca Gold', 'Ypióca Empalhada Gold',
        'Canelinha da Roça'
    ],
    'Frios': [
        'Mussarela', 'Presunto', 'Mortadela', 'Lombinho', 'Bacon'
    ],
    'Bebidas': [
        'Chá Leão 300mL pêssego', 'Suco Del Valle uva 450mL', 'Suco Del Valle laranja 450mL',
        'Energético Monster Trad. 473mL', 'Energético Monster zero 473mL', 'Energético Monster pêssego 473mL',
        'Isotônico Powerade targ.', 'Isotônico Powerade azul', 'Isotônico Powerade uva',
        'Água sem gás 500mL Crystal', 'Água sem gás 300mL Minalice', 'Suco laranja nativo 500mL',
        'Suco nativo de uva', 'Água com gás 500mL Crystal', 'Água com gás 1,5L Crystal',
        'Água sem gás 1,5L Crystal', 'Suco Del Valle 1,5L pêssego', 'Suco Del Valle 1,5L laranja',
        'Suco Del Valle 1,5L uva', 'Suco Kapo morango', 'Suco Kapo uva', 'Vinho Chapinha',
        'Vinho Mioranza', 'Vinho Santo Expedito'
    ],
    'Laticínios': [
        'Leite integral 1L Italac', 'Leite integral 1L Jussara', 'Margarina Qualy 250g',
        'Requeijão', 'Leite condensado Piracanjuba', 'Creme de leite Piracanjuba'
    ],
    'Matinais': [
        'Pão francês', 'Pão de forma Bauducco', 'Pão de forma São Sebastião', 'Nescau lata 380g',
        'Nescau lata 350g', 'Café Terreiro'
    ],
    'Alimentos': [
        'Açúcar Santa Isabel 1kg', 'Farinha Nita 1kg', 'Farinha Nita cook chocolate',
        'Farinha Nita cook laranja', 'Farinha Nita cook fubá', 'Fubá Mimoso Sinhá',
        'Farinha mandioca queimada Selka', 'Farinha de milho Selka', 'Óleo de cozinha Soya / Brejeiro',
        'Vinagre sem álcool Castelo', 'Sal refinado União', 'Sal grosso Master Grill',
        'Miojo Volle carne', 'Miojo Volle galinha', 'Miojo Volle galinha caipira',
        'Macarrão Basilar espaguete', 'Macarrão Basilar ave maria', 'Macarrão Basilar parafuso',
        'Macarrão Basilar penne', 'Macarrão Basilar padre nosso', 'Massa Tipo lasanha Caseira',
        'Massa Tipo macarrão Caseira', 'Fugini milho', 'Bolacha Nikito chocolate',
        'Bolacha Nikito chocolate c/ morango', 'Bolacha Bono chocolate', 'Bolacha Negresco',
        'Rosquinha Dallas sabor coco', 'Bolacha Água e Sal Tues', 'Bolacha Passa Tempo',
        'Waffle Bauducco chocolate', 'Waffle Bauducco morango', 'Torradas Bauducco',
        'Triunfo bolacha maizena', 'Triunfo bolacha água e sal', 'Bauducco Roll',
        'Bauducco Duo Fini', 'Bauducco bolinho de chocolate', 'Bauducco bolinho de brigadeiro',
        'Milho de pipoca Sinhá', 'Milho de pipoca Kinino', 'Pipoca de microondas Yoki cinema',
        'Pipoca de microondas Yoki bacon', 'Pipoca de microondas Yoki temperada',
        'Farofa Ravitos costela', 'Farofa Ravitos extra picante', 'Fermento em pó Nita',
        'Coco ralado Menina', 'Leite de coco Menina', 'Queijo ralado Palminio'
    ],
    'Molhos e Condimentos': [
        'Molhos de pimenta Asteca', 'Molhos de pimenta Gota', 'Molhos de pimenta Radja',
        'Tempero Sabor Sazon carne', 'Caldo sabor galinha Maggi', 'Caldo Knorr sabor galinha',
        'Colorau', 'Chocolate (pó)', 'Camomila', 'Pimenta', 'Canela', 'Canela pó',
        'Bicarbonato', 'Orégano', 'Erva-doce', 'Louro', 'Molho de tomate Pomarola',
        'Molho de tomate Fugini', 'Extrato de tomate Elefante', 'Maionese Hellmann\'s',
        'Maionese Heinz', 'Ketchup Heinz', 'Molho de pimenta Asteca', 'Molho de pimenta Gota',
        'Molho de pimenta Ravitos'
    ],
    'Conserva': [
        'Palmito 300g Predilecta', 'Palmito 560g Predilecta', 'Azeitona Tozzi sem caroço',
        'Azeitona Tozzi fatiada', 'Azeitona Tatá fatiada', 'Fugini seleta', 'Predilecta ervilha',
        'Salsicha em conserva'
    ],
    'Bazar e Utilidades': [
        'Papel toalha Yuri', 'Maço de fósforo Fiat Lux / Paraná', 'Caixa de fósforo',
        'Copos descartáveis', 'Velas São Domingos', 'Papel Melitta (filtro de café)',
        'Maço de fósforo Guarany'
    ]
}

try:
    conexao = psycopg2.connect(
        user=DB_USER, host=DB_HOST, port=DB_PORT, database=DB_NAME
    )
    cursor = conexao.cursor()
    print("Conexão realizada com sucesso! Prontos para inserir.")

    # NOVO: Remove a tabela antiga para aplicar as novas regras sem dar erro de conflito
    cursor.execute("DROP TABLE IF EXISTS produtos CASCADE;")

    # A) Cria a tabela de produtos do zero com a regra UNIQUE atualizada
    cursor.execute('''
    CREATE TABLE produtos (
        id SERIAL PRIMARY KEY,  
        nome VARCHAR(150) NOT NULL,
        categoria_id INTEGER REFERENCES categorias(id) ON DELETE CASCADE,
        CONSTRAINT produto_unico UNIQUE (nome, categoria_id)
    );
    ''')

    # B) Insere as categorias no banco de dados
    for categoria in lista_categorias:
        cursor.execute(
            "INSERT INTO categorias (nome) VALUES (%s) ON CONFLICT DO NOTHING;",
            (categoria,)
        )

    # C) Inserção dos produtos vinculados aos IDs das categorias
    print("Iniciando a inserção dos produtos...")

    for nome_categoria, lista_produtos in produtos_por_categoria.items():
        cursor.execute("SELECT id FROM categorias WHERE nome = %s;", (nome_categoria,))
        resultado = cursor.fetchone()

        if resultado:
            categoria_id = resultado[0]

            for nome_produto in lista_produtos:
                cursor.execute("""
                    INSERT INTO produtos (nome, categoria_id) 
                    VALUES (%s, %s) 
                    ON CONFLICT ON CONSTRAINT produto_unico DO NOTHING;
                """, (nome_produto, categoria_id))

    # Confirma todas as alterações no banco de dados
    conexao.commit()
    print("Tudo pronto! Tabelas criadas, categorias e produtos salvos com sucesso!")

except Exception as erro:
    print(f"Ocorreu um erro: {erro}")

finally:
    if 'conexao' in locals() and conexao:
        cursor.close()
        conexao.close()
        print("Conexão com o banco de dados fechada.")
