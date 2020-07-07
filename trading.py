#!./env/bin/python

import sqlite3

# import random

# import yahoo_fin.stock_info
from yahoo_fin.stock_info import get_live_price
import time
import os

import sys

import datetime

STOCK = sys.argv[1]
# STOCK = "EURUSD=X"
DATABASE = "datos.sqlite3"


def db_query(query, *args):
    con = None
    data = None

    try:
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute(query, tuple(args))
        data = cur.fetchall()
        if not data:
            con.commit()
    except sqlite3.Error as e:
        # self.log.error("Database error: %s" % e)
        print("Database error: %s" % e)
    except Exception as e:
        # self.log.error("Exception in _query: %s" % e)
        print("Exception in _query: %s" % e)
    finally:
        if con:
            con.close()
    return data


try:
    sql_load = "SELECT * FROM datos WHERE stock=?  ORDER BY id DESC LIMIT 1"
    row = db_query(sql_load, STOCK)
    balance = row[2]
    stop_value = row[3]
    value_each_purchase = row[4]
    buying_times = row[5]
    winning_sales = row[6]
    loosing_sales = row[7]
    earned_money = row[8]
    commission_broker = row[9]
    total_fees_broker = row[10]
    stock = STOCK
    purchased_items = row[12]
# price_now = row[12]
except Exception:
    balance = 1000000
    stop_value = 100
    value_each_purchase = 100000
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
    while True:
        # Get new price for the stock
        price_now = get_live_price(STOCK)

        # Buy
        if purchased_items <= 0:
            value_position_now = value_each_purchase / price_now
            purchased_items = value_position_now
            balance -= value_position_now + commission_broker
            buying_times += 1
            total_fees_broker += commission_broker
            earned_money -= commission_broker

        value_position_now = price_now * purchased_items

        # Sell winning
        if value_position_now > value_each_purchase + (2 * stop_value):
            balance += value_position_now - commission_broker
            earned_money += value_position_now - value_each_purchase
            purchased_items = 0
            winning_sales += 1
            total_fees_broker += commission_broker

        # Sell loosing
        if value_position_now < value_each_purchase - stop_value:
            balance += value_position_now - commission_broker
            earned_money += value_position_now - value_each_purchase
            purchased_items = 0
            loosing_sales += 1
            total_fees_broker += commission_broker

        os.system("clear")
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

        # Insert values in DB table, values
        sql_insert = """INSERT INTO datos (balance, stop_value, value_each_purchase, buying_times,
        winning_sales, loosing_sales,
        earned_money, commission_broker, total_fees_broker, stock, price_now, purchased_items)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              """
        db_query(
            sql_insert,
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
        time.sleep(10)

except KeyboardInterrupt:
    pass
