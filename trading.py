#!./env/bin/python

import sqlite3

# import random

# import yahoo_fin.stock_info
from yahoo_fin.stock_info import get_live_price
import time

import os
import math
import sys
import numpy as np
import datetime

use_db = 0
item = sys.argv[1]
# item = "KO"
# item = "EURUSD=X"
DATABASE = "datos.sqlite3"
portfolio = {}
portfolio[item] = 0
paid_position = {}

# Init variables
balance = 1000000
stop_value = 100
value_each_purchase = 100000
buying_times = 0
winning_sales = 0
loosing_sales = 0
earned_money = 0
commission_broker = 2.0
total_fees_broker = 0
stock = item
purchased_items = 0


def cls():
    os.system("clear")


# def cls():
#    print("\n" * 100)


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


if use_db:
    try:
        sql_load = "SELECT * FROM datos WHERE stock=?  ORDER BY id DESC LIMIT 1"
        row = db_query(sql_load, item)
        balance = row[2]
        stop_value = row[3]
        value_each_purchase = row[4]
        buying_times = row[5]
        winning_sales = row[6]
        loosing_sales = row[7]
        earned_money = row[8]
        commission_broker = row[9]
        total_fees_broker = row[10]
        stock = item
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
        stock = item
        purchased_items = 0


startTime = datetime.datetime.now()


def buy(item, value_each_purchase):
    global balance, portfolio, total_fees_broker, earned_money
    global buying_times, paid_position

    price = get_live_price(item)
    if not np.isnan(price):
        quantity = math.floor(value_each_purchase / price)
        paid_position[item] = (quantity * price) + commission_broker
        balance -= paid_position[item]
        if item in portfolio:
            portfolio[item] += quantity
        else:
            portfolio[item] = quantity
        total_fees_broker += commission_broker
        earned_money -= commission_broker
        buying_times += 1


def sell(item, quantity):
    global balance, portfolio, total_fees_broker, earned_money
    global winning_sales, loosing_sales, paid_position

    price = get_live_price(item)
    if not np.isnan(price):
        balance += (quantity * price) - commission_broker
        portfolio[item] -= quantity
        total_fees_broker += commission_broker
        operation_value = (quantity * price) - paid_position[item] - commission_broker
        earned_money += operation_value
        if operation_value < 0:
            loosing_sales += 1
        else:
            winning_sales += 1


def strategy(item):
    price = get_live_price(item)

    if portfolio[item] == 0:
        buy(item, value_each_purchase)

    if item in portfolio:
        value_position_now = portfolio[item] * price

    if value_position_now > paid_position[item] + (2 * stop_value):
        sell(item, portfolio[item])

    if value_position_now < paid_position[item] - stop_value:
        sell(item, portfolio[item])


def main():
    while True:
        # global item
        strategy(item)
        price_now = get_live_price(item)
        value_position_now = portfolio[item] * price_now

        cls()

        # os.system("clear")
        print(
            f"Balance {balance:,.2f}\n\
Price of {stock} now: {price_now:,.4f}\n\
Number of {stock} Bought: {portfolio[item]:,.2f}\n\
Value {stock} when bought: {paid_position[item]:,.2f}\n\
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

        if use_db:
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


if __name__ == "__main__":
    main()
