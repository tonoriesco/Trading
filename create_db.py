import sqlite3

DATABASE = "datos.sqlite3"

con = sqlite3.connect(DATABASE)
cur = con.cursor()

create_table = """
CREATE TABLE  IF NOT EXISTS datos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    balance REAL DEFAULT 1000000,
    valor_stop REAL DEFAULT 100,
    objetos_comprados INTEGER DEFAULT 0,
    compra INTEGER DEFAULT 100000,
    compras INTEGER DEFAULT 0,
    ventas_ganadoras INTEGER DEFAULT 0,
    ventas_perdedoras INTEGER DEFAULT 0,
    ganancia_total REAL DEFAULT 0,
    comision REAL DEFAULT 2.0,
    comisiones REAL DEFAULT 0,
    moneda TEXT
    )
"""
cur.execute(create_table)
