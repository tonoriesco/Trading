#!/usr/bin/env python3

import sqlite3
import random

# import yahoo_fin.stock_info
from yahoo_fin.stock_info import get_live_price
import time
import os
from datetime import datetime

DATABASE = "datos.sqlite3"

balance = 1000000
valor_stop = 100
objetos_comprados = 0
compras = 0
compra = 100000
ventas_ganadoras = 0
ventas_perdedoras = 0
ganancia_total = 0
comision = 2.0
comisiones = 0
moneda = "BTC"


def do_query(path, query, one=True, args=None, commit=False):
    """
    do_query - Run a SQLite query, waiting for DB in necessary

    Args:
        path (str): path to DB file
        query (str): SQL query
        one (bool): if True, get ony one row, if False, all rows
        args (list): values for `?` placeholders in qquery
        commit (bool): whether or not to commit after running query
    Returns:
        list of lists: fetchall() for the query
    """
    if args is None:
        args = []
    for attempt in range(3):
        try:
            con = sqlite3.connect(path)
            cur = con.cursor()
            cur.execute(query, args)
            if one:
                ans = cur.fetchone()
            else:
                ans = cur.fetchall
            if commit:
                con.commit()
            cur.close()
            con.close()
            del cur
            del con
            return ans
        except sqlite3.OperationalError:
            time.sleep(random.randint(1, 3))


def insert_values(task):
    """
    Create a new task
    :param task:
    :return: last id from table
    """
    sql = """INSERT INTO datos(balance, valor_stop, objetos_comprados,
        compra ,compras, ventas_ganadoras, ventas_perdedoras,
        ganancia_total, comision, comisiones, moneda)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(sql, task)
    con.commit()
    cur.close()
    con.close()
    return cur.lastrowid


# con = sqlite3.connect(DATABASE)
# cur = con.cursor()


sql_load = "SELECT * FROM datos ORDER BY id DESC LIMIT 1"
row = do_query(DATABASE, sql_load)

# cur.execute(sql_load)
# row = cur.fetchone()
# if con:
#     con.close()
# # with open("data.json") as data_json:
# #     var_read = json.load(data_json)

balance = row[2]
valor_stop = row[3]
objetos_comprados = row[4]
compra = row[5]
compras = row[6]
ventas_ganadoras = row[7]
ventas_perdedoras = row[8]
ganancia_total = row[9]
comision = row[10]
comisiones = row[11]
moneda = row[12]


startTime = datetime.now()

try:
    while True:
        precio_actual = get_live_price("BTC-USD")

        # Compra
        if objetos_comprados <= 0:
            objetos_comprados = compra / precio_actual
            balance -= compra + comision
            compras += 1
            comisiones += comision
            ganancia_total -= comision

        valor_btc_ahora = precio_actual * objetos_comprados

        # Venta ganancia
        if valor_btc_ahora > compra + (2 * valor_stop):
            balance += valor_btc_ahora - comision
            ganancia_total += valor_btc_ahora - compra
            objetos_comprados = 0
            ventas_ganadoras += 1
            comisiones += comision

        # Venta perdida
        if valor_btc_ahora < compra - valor_stop:
            balance += valor_btc_ahora - comision
            ganancia_total += valor_btc_ahora - compra
            objetos_comprados = 0
            ventas_perdedoras += 1
            comisiones += comision

        os.system("clear")
        print(
            f"Balance {balance:,.2f} EUR\n\
Precio {moneda} ahora: {precio_actual:,.2f} EUR\n\
{moneda} Comprados: {objetos_comprados:,.2f} {moneda}\n\
Valor {moneda} a la compra: {compra:,.2f} EUR\n\
Valor {moneda} ahora: {valor_btc_ahora:,.2f} EUR\n\
Compras: {compras}\n\
Comision por operacion: {comision:,.2f} EUR\n\
Comisiones Totales: {comisiones:,.2f} EUR\n\
Ventas Ganadoras: {ventas_ganadoras} \n\
Ventas Perdedoras: {ventas_perdedoras} \n\
Ganacias hasta ahora: {ganancia_total:,.2f} EUR\n\
Tiempo corriendo: {datetime.now() - startTime}\n\
        "
        )

        valores = (
            balance,
            valor_stop,
            objetos_comprados,
            compra,
            compras,
            ventas_ganadoras,
            ventas_perdedoras,
            ganancia_total,
            comision,
            comisiones,
            moneda,
        )

        insert_values(valores)

        time.sleep(60)

except KeyboardInterrupt:
    pass
