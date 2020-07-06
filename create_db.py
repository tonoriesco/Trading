import sqlite3

DATABASE = "datos.sqlite3"

con = sqlite3.connect(DATABASE)
cur = con.cursor()

create_table = """
CREATE TABLE IF NOT EXISTS "datos" (
    "id"    INTEGER,
    "date"    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "balance"    REAL DEFAULT 1000000,
    "stop_value"    REAL DEFAULT 100,
    "value_each_purchase"    INTEGER DEFAULT 100000,
    "buying_times"    INTEGER DEFAULT 0,
    "winning_sales"    INTEGER DEFAULT 0,
    "loosing_sales"    INTEGER DEFAULT 0,
    "earned_money"    REAL DEFAULT 0,
    "commission_broker"    REAL DEFAULT 2.0,
    "total_fees_broker"    REAL DEFAULT 0,
    "stock"    TEXT DEFAULT 'APPL',
    "price_now"    REAL DEFAULT 100.00,
    "purchased_items"    REAL DEFAULT 0,
    PRIMARY KEY("id" AUTOINCREMENT)
);
"""
cur.execute(create_table)
