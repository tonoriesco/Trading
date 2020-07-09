#!./env/bin/python
import argparse
import sqlite3

# import random
# import yahoo_fin.stock_info
from yahoo_fin.stock_info import get_live_price
import time
import os
import math
import yaml
import sys
import numpy as np
import datetime


parser = argparse.ArgumentParser(
    description="Trade a stock, currency pair, etc getting the values from Yahoo."
)
parser.add_argument(
    "-i",
    "--item",
    dest="item",
    required=True,
    metavar="(stock|index|forex pair)",
    type=str,
    help="The item you want to trade, e.g., EURUSD=X or KO, TEF.MC etc.\n\
        The items must be checked in the https://finance.yahoo.com/quote/VALUE\n\
        If the item is not in Yahoo the program will not run\n",
)
parser.add_argument(
    "-d",
    "--database",
    dest="db",
    metavar="DB sqlite3 file",
    type=str,
    help="\nSpecify the database that will be used to store the runs. (default: Don't use a database)\n\n",
)
parser.add_argument(
    "-f",
    "--file",
    dest="para",
    required=False,
    type=str,
    metavar="configuration file",
    help="\nIf present, the file parameters.yaml is read and the values are taken from there.\n\
        (default: Take the values from DB or defaults if doesn't exist old data)\n\n",
)

args = parser.parse_args()
database = args.db
item = args.item
para_file = args.para
# use_db = 1
# item = "EURUSD=X"

# item = sys.argv[1]
# item = "KO"
# item = "EURUSD=X"
portfolio = {}
portfolio[item] = 0
paid_position = {}


# Init internal variables
buying_times = 0
winning_sales = 0
loosing_sales = 0
earned_money = 0
total_fees_broker = 0

startTime = datetime.datetime.now()


def cls():
    os.system("clear")


# def cls():
#    print("\n" * 100)


def db_query(query, *args):
    con = None
    data = None

    try:
        con = sqlite3.connect(database)
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
        print("Exception in query: %s" % e)
    finally:
        if con:
            con.close()
    return data


def load_default():
    balance = 1000000
    stop_value = 100
    value_each_purchase = 100000
    buying_times = 0
    winning_sales = 0
    loosing_sales = 0
    earned_money = 0
    commission_broker = 2
    total_fees_broker = 0
    # item = "EURUSD=X"
    portfolio[item] = 0
    paid_position[item] = 0
    database = "data.sqlite3"
    globals().update(locals())


def load_file():
    try:
        with open(para_file, "r") as f:
            vars = yaml.load(f, Loader=yaml.FullLoader)
        stop_value = vars["stop_value"]
        value_each_purchase = vars["value_each_purchase"]
        commission_broker = vars["commission_broker"]
        balance = vars["balance"]
        database = vars["database"]
        globals().update(locals())

    except Exception:
        print("Error in parameter's file, loading from DB or defaults")
        time.sleep(2)
        load_from_db()


def load_from_db():
    try:
        sql_load = "SELECT * FROM data WHERE item=?  ORDER BY id DESC LIMIT 1"
        row = db_query(sql_load, item)
        balance = row[0][2]
        stop_value = row[0][3]
        value_each_purchase = row[0][4]
        buying_times = row[0][5]
        winning_sales = row[0][6]
        loosing_sales = row[0][7]
        earned_money = row[0][8]
        commission_broker = row[0][9]
        total_fees_broker = row[0][10]
        portfolio[item] = row[0][13]
        paid_position[item] = row[0][14]
        globals().update(locals())

    # price_now = row[0][12]
    except Exception:
        load_default()
        print("No old data in de DB, loading defaults")
        time.sleep(2)


if para_file:
    load_file()
elif database:
    load_from_db()
else:
    load_default()


def buy(item, value_each_purchase):
    global balance, portfolio, total_fees_broker, earned_money
    global buying_times, paid_position, commission_broker

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
        return paid_position[item]


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
    global value_each_purchase, stop_value
    price = get_live_price(item)
    if portfolio[item] == 0:
        paid_position[item] = buy(item, value_each_purchase)
    if item in portfolio:
        value_position_now = portfolio[item] * price
    if value_position_now > paid_position[item] + (2 * stop_value):
        sell(item, portfolio[item])

    if value_position_now < paid_position[item] - stop_value:
        sell(item, portfolio[item])


def main():
    # first of all check if the symbol is found in Yahoo Finance, if not, stop and show the result
    try:
        get_live_price(item)
        # print(f"Connected to Yahoo\nGot {df} values\n")
    except Exception as e:

        print(f"\nThere is an error. The symbol was not found.\nDescription: {e}\n")
        sys.exit(0)
        # raise
    try:

        while True:
            # global item
            strategy(item)
            price_now = get_live_price(item)
            value_position_now = portfolio[item] * price_now

            cls()
            # To clean the milliseconds in calculations
            time_running = str(datetime.datetime.now() - startTime).split(".")[0]

            # os.system("clear")
            print(f"Balance {balance:,.2f}")
            print(f"Price of {item} now: {price_now:,.4f}")
            print(f"Number of {item} Bought: {portfolio[item]:,.2f}")
            print(f"Value {item} when bought: {paid_position[item]:,.2f}")
            print(f"Value {item} now: {value_position_now:,.2f}")
            print(f"Number of buys: {buying_times}")
            print(f"Commission Broker: {commission_broker:,.2f}")
            print(f"Total Commision Paid: {total_fees_broker:,.2f}")
            print(f"Winning Sales: {winning_sales} ")
            print(f"Loosing Sales: {loosing_sales} ")
            print(f"Earned Money: {earned_money:,.2f}")
            print(f"Time running the program: {time_running}")
            print("Press (Crtl + C) to stop.")

            if database:
                # Insert values in DB table, values
                sql_insert = """INSERT INTO data (balance, stop_value, value_each_purchase, buying_times,
                winning_sales, loosing_sales, earned_money, commission_broker, total_fees_broker,
                item, price_now, purchased_items, price_paid)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    item,
                    price_now,
                    portfolio[item],
                    paid_position[item],
                )
            time.sleep(60)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
