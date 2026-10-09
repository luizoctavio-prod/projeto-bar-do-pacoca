# Sistema de Gestão - Bar do Paçoca

Sistema em Python e PostgreSQL para controle de estoque e vendas, desenvolvido
pensando nas necessidades de um estabelecimento real que funciona como bar e
mercearia.

## Funcionalidades
- Cadastro e organização de produtos por categoria
- Listagem de produtos com estoque atual
- Atualização de produtos (preço, estoque)
- Registro de vendas
- Relatório de estoque em formato de tabela no terminal

## Tecnologias
- Python 3
- PostgreSQL
- psycopg2 (conexão com o banco)
- tabulate (relatórios no terminal)

## Como rodar
1. Clone o repositório e crie um ambiente virtual:
```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
```
2. Crie o banco `mercearia_db` no PostgreSQL.
3. Ajuste as credenciais de conexão em `Banco.py`.
4. Carregue as tabelas e os produtos iniciais:
```
   python categorias.py
```
5. Rode o script desejado, por exemplo:
```
   python relatorio.py
```

## Estrutura
- `Banco.py`: conexão com o banco
- `schema.sql`: estrutura das tabelas (documentação do banco)
- `evoluir_banco.py`: evolução das tabelas
- `categorias.py`: criação de categorias e carga inicial de produtos
- `listar_produtos.py`: listagem de produtos
- `atualizar_produtos.py`: atualização de produtos
- `realizar_vendas.py`: registro de vendas
- `relatorio.py`: relatório de estoque

## Status
Em desenvolvimento. Próximos passos:
- [ ] Menu único para acessar todas as funções
- [ ] Tabelas de vendas e relatórios de faturamento
- [ ] Interface web ou API