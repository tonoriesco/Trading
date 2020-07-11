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

# Init variables with defaults
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
purchased_items = 0
paid_position = 0
database = "data.db"
value_position_now = 0
purchased_items = 0
value_position_now = 0
# Init internal variables
buying_times = 0
winning_sales = 0
loosing_sales = 0
earned_money = 0
total_fees_broker = 0

startTime = datetime.datetime.now()


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
        (default: Take the values from DB or defaults if doesn't exist old data in the DB)\n\n",
)

args = parser.parse_args()
database = args.db
item = args.item
para_file = args.para


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
        purchased_items = row[0][13]
        paid_position = row[0][14]
        globals().update(locals())

    # price_now = row[0][12]
    except Exception:
        print("No old data in de DB, loading defaults")
        time.sleep(2)


# If the file exists, take the values from there. If not, try from the DB

if para_file:
    load_file()
else:
    load_from_db()


def buy(item, value_each_purchase):
    global balance, portfolio, total_fees_broker, earned_money
    global buying_times, paid_position, commission_broker, purchased_items

    price = get_live_price(item)
    if not np.isnan(price):
        quantity = math.floor(value_each_purchase / price)
        paid_position = (quantity * price) + commission_broker
        balance -= paid_position
        if purchased_items:
            purchased_items += quantity
        else:
            purchased_items = quantity
        total_fees_broker += commission_broker
        earned_money -= commission_broker
        buying_times += 1
        return paid_position


def sell(item, quantity):
    global balance, portfolio, total_fees_broker, earned_money
    global winning_sales, loosing_sales, paid_position, purchased_items

    price = get_live_price(item)
    if not np.isnan(price):
        balance += (quantity * price) - commission_broker
        purchased_items -= quantity
        total_fees_broker += commission_broker
        operation_value = (quantity * price) - paid_position - commission_broker
        earned_money += operation_value
        if operation_value < 0:
            loosing_sales += 1
        else:
            winning_sales += 1


def strategy(item):
    global stop_value, SMA100, SMA20

    ##############################################################
    # price = get_live_price(item)
    # if purchased_items == 0:
    #    paid_position = buy(item, value_each_purchase)
    # if value_position_now:
    #    value_position_now = purchased_items * price
    #    if value_position_now > paid_position + (2 * stop_value):
    #        sell(item, purchased_items)

    #    if value_position_now < paid_position - stop_value:
    #        sell(item, purchased_items)
    ##############################################################

    SMA_list_100 = db_query(
        f"SELECT avg(price_now) FROM data WHERE item = '{item}' and time(date) > time('now','-100 minutes');"
    )
    SMA_list_20 = db_query(
        f"SELECT avg(price_now) FROM data WHERE item = '{item}' and time(date) > time('now','-20 minutes');"
    )
    if SMA_list_100 and SMA_list_20:
        SMA20 = SMA_list_20[0][0]
        SMA100 = SMA_list_100[0][0]
        value_position_now = get_live_price(item) * purchased_items

        if SMA20 and SMA100:
            if SMA20 < SMA100 and value_position_now > 0:
                sell(item, purchased_items)

            if SMA20 > SMA100 and value_position_now < value_each_purchase:
                buy(item, (value_each_purchase - value_position_now))


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
            value_position_now = purchased_items * price_now

            # os.system("clear")
            # To clean the milliseconds in calculations
            time_running = str(datetime.datetime.now() - startTime).split(".")[0]

            os.system("clear")
            print(f"Balance {balance:,.2f}")
            print(f"Price of {item} now: {price_now:,.4f}")
            print(f"Number of {item} Bought: {purchased_items:,.2f}")
            print(f"Value of position when bought: {paid_position:,.2f}")
            print(f"Value of position now: {value_position_now:,.2f}")
            print(f"Commission Broker: {commission_broker:,.2f}")
            print(f"Total Commission Paid: {total_fees_broker:,.2f}")
            print(f"Number of buys: {buying_times}")
            print(f"Winning Sales: {winning_sales} ")
            print(f"Loosing Sales: {loosing_sales} ")
            print(f"Earned Money: {earned_money:,.2f}")
            print(f"Time running the program: {time_running}")
            print(f"SMA20 - SMA100: {(SMA20 - SMA100):,.4f}")
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
                    purchased_items,
                    paid_position,
                )
            time.sleep(60)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
