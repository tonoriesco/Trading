#!/usr/bin/env python3

import sqlite3

# import random

# import yahoo_fin.stock_info
# from yahoo_fin.stock_info import get_live_price
# import time
import os

import sys
import datetime

# from datetime import datetime

STOCK = sys.argv[1]
# STOCK = "EURUSD=X"
DB_OPERATION = "backtesting.db"
DB_DATOS = "stock.db"


def db_query(db, query, *args):
    con = None
    data = None

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(query, tuple(args))
        data = cur.fetchall()
        if not data:
            con.commit()
    except sqlite3.Error as e:
        # self.log.error("DB_OPERACION error: %s" % e)
        print("DB_OPERACION error: %s" % e)
    except Exception as e:
        # self.log.error("Exception in _query: %s" % e)
        print("Exception in _query: %s" % e)
    finally:
        if con:
            con.close()
    return data


balance = 100000
stop_value = 100
value_each_purchase = 10000
buying_times = 0
winning_sales = 0
loosing_sales = 0
earned_money = 0
commission_broker = 2.0
total_fees_broker = 0
stock = STOCK
purchased_items = 0


startTime = datetime.datetime.now()

try:

    # Get new price for the stock from DB_OPERACION
    sql_load = f"SELECT * FROM '{STOCK}'"
    rows = db_query(DB_DATOS, sql_load)
    i = 0

    for row in rows:
        i += 1
        print(f"  Days runned: {i}\r", end="")
        # price_now = get_live_price(STOCK)
        price_date = row[1]
        price_now = row[2]
        # Compra
        if purchased_items <= 0:
            purchased_items = value_each_purchase / price_now
            balance -= (purchased_items * price_now) + commission_broker
            buying_times += 1
            total_fees_broker += commission_broker
            earned_money -= commission_broker

        value_position_now = purchased_items * price_now

        # Venta ganancia
        if value_position_now > (value_each_purchase + (2 * stop_value)):
            balance += value_position_now - commission_broker
            earned_money += value_position_now - value_each_purchase - commission_broker
            purchased_items = 0
            winning_sales += 1
            total_fees_broker += commission_broker

        # Venta perdida
        if value_position_now < (value_each_purchase - stop_value):
            balance += value_position_now - commission_broker
            earned_money += value_position_now - value_each_purchase - commission_broker
            purchased_items = 0
            loosing_sales += 1
            total_fees_broker += commission_broker

        # Insert values in DB table, values
        sql_insert = """INSERT INTO datos (date, balance, stop_value, value_each_purchase, buying_times,
        winning_sales, loosing_sales,
        earned_money, commission_broker, total_fees_broker, stock, price_now, purchased_items)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        db_query(
            DB_OPERATION,
            sql_insert,
            price_date,
            balance,
            stop_value,
            value_each_purchase,
            buying_times,
            winning_sales,
            loosing_sales,
            earned_money,
            commission_broker,
            total_fees_broker,
            stock,
            price_now,
            purchased_items,
        )
        # time.sleep(1)

except KeyboardInterrupt:
    pass
os.system("clear")

# Sell last position
balance += value_position_now - commission_broker
print(
    f"Balance {balance:,.2f}\n\
Price of {stock} now: {price_now:,.4f}\n\
{stock} Bought: {purchased_items:,.2f}\n\
Value {stock} when bought: {value_each_purchase:,.2f}\n\
Value {stock} now: {value_position_now:,.2f}\n\
Number of buys: {buying_times}\n\
Commission Broker: {commission_broker:,.2f}\n\
Total Commision Paid: {total_fees_broker:,.2f}\n\
Winning Sales: {winning_sales} \n\
Loosing Sales: {loosing_sales} \n\
Earned Money: {earned_money:,.2f}\n\
Time running the backtesting: {datetime.datetime.now() - startTime}\n\
        "
)
