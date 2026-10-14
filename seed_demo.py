"""Gera dados FICTÍCIOS de vendas para demonstração do sistema.

Uso:
    python seed_demo.py --limpar      # apaga TODAS as vendas
    python seed_demo.py               # gera 30 dias de vendas fictícias
    python seed_demo.py --dias 60     # gera 60 dias
"""
import argparse
import os
import random
from datetime import datetime, timedelta
from decimal import Decimal

import psycopg2
from dotenv import load_dotenv

load_dotenv()
random.seed(42)  # mesmos dados a cada execução

HORAS = list(range(10, 24))
PESOS_HORAS = [1, 1, 2, 2, 2, 2, 3, 5, 7, 9, 9, 6, 3, 1]  # pico à noite
MOVIMENTO_POR_DIA = {4: 50, 5: 60, 6: 30}  # sex, sáb, dom (padrão: 20)


def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        dbname=os.getenv("DB_NAME", "mercearia_db"),
    )


def limpar(conn):
    resp = input("Isso apaga TODAS as vendas. Digite 'sim' para continuar: ")
    if resp.strip().lower() != "sim":
        print("Cancelado.")
        return
    with conn.cursor() as cur:
        cur.execute("TRUNCATE itens_venda, vendas RESTART IDENTITY;")
    conn.commit()
    print("Vendas apagadas.")


def gerar(conn, dias):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM vendas;")
        if cur.fetchone()[0] > 0:
            print("Já existem vendas. Rode antes: python seed_demo.py --limpar")
            return

        cur.execute("SELECT id, preco FROM produtos ORDER BY id;")
        todos = cur.fetchall()
        if not todos:
            print("Nenhum produto cadastrado.")
            return

        # 40 produtos "ativos", com popularidade decrescente
        ativos = random.sample(todos, min(40, len(todos)))
        ids = [pid for pid, _ in ativos]
        pesos = [1 / (i + 1) for i in range(len(ids))]
        precos = {}
        for pid, preco in ativos:
            if preco == 0:  # preço fictício, só onde ainda não há preço
                preco = Decimal(random.randrange(300, 6000, 50)) / 100
                cur.execute("UPDATE produtos SET preco = %s WHERE id = %s;",
                            (preco, pid))
            precos[pid] = Decimal(preco)

        hoje = datetime.now().replace(hour=0, minute=0, second=0,
                                      microsecond=0)
        qtd_vendas = 0
        faturamento = Decimal("0")

        for d in range(dias, 0, -1):
            dia = hoje - timedelta(days=d)
            base = MOVIMENTO_POR_DIA.get(dia.weekday(), 20)
            for _ in range(max(1, int(base * random.uniform(0.7, 1.3)))):
                n_itens = random.choices([1, 2, 3, 4], [50, 30, 15, 5])[0]
                escolhidos = set(random.choices(ids, weights=pesos, k=n_itens))
                itens = [(pid, random.choices([1, 2, 3], [70, 22, 8])[0],
                          precos[pid]) for pid in escolhidos]
                total = sum(p * q for _, q, p in itens)
                momento = dia + timedelta(
                    hours=random.choices(HORAS, PESOS_HORAS)[0],
                    minutes=random.randrange(60),
                    seconds=random.randrange(60),
                )
                cur.execute(
                    "INSERT INTO vendas (data_hora, total) VALUES (%s, %s) "
                    "RETURNING id;", (momento, total))
                venda_id = cur.fetchone()[0]
                for pid, qtd, preco in itens:
                    cur.execute(
                        "INSERT INTO itens_venda "
                        "(venda_id, produto_id, quantidade, preco_unitario) "
                        "VALUES (%s, %s, %s, %s);",
                        (venda_id, pid, qtd, preco))
                qtd_vendas += 1
                faturamento += total

        # Estoque atual fictício dos produtos ativos
        for pid in ids:
            cur.execute("UPDATE produtos SET estoque = %s WHERE id = %s;",
                        (random.randint(5, 80), pid))

    conn.commit()
    print(f"{qtd_vendas} vendas fictícias geradas em {dias} dias "
          f"(faturamento simulado: R$ {faturamento:.2f}).")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dias", type=int, default=30)
    parser.add_argument("--limpar", action="store_true")
    args = parser.parse_args()

    conn = conectar()
    try:
        if args.limpar:
            limpar(conn)
        else:
            gerar(conn, args.dias)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()