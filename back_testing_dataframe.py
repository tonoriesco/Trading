#!/usr/bin/env python3


# import yahoo_fin.stock_info

# from yahoo_fin.stock_info import get_live_price
# import time
# import pandas as pd
from pandas_datareader import data
import os

import sys
import datetime

# from datetime import datetime

# pretty printing of pandas dataframe
# pd.set_option("expand_frame_repr", False)
# for pandas_datareader, sometimes there can be version mismatch
# pd.core.common.is_list_like = pd.api.types.is_list_like

STOCK = sys.argv[1]
# STOCK = "KO"

start_time = datetime.datetime(2010, 1, 1)
# end_time = datetime.datetime(2019, 1, 20)
end_time = datetime.datetime.now().date().isoformat()  # today


balance = 1000000
stop_value = 1000
risk_ratio = 2
value_each_purchase = 100000
buying_times = 0
winning_sales = 0
loosing_sales = 0
earned_money = 0
commission_broker = 2.0
total_fees_broker = 0
stock = STOCK
purchased_items = 0

# get daily stock data from yahoo API
connected = False
while not connected:
    try:
        df = data.DataReader(
            STOCK, start=start_time, end=end_time, data_source="yahoo"
        )["Close"]
        connected = True
        # print(f"Connected to Yahoo\nGot {df} values\n")
    except Exception as e:
        print("type error: " + str(e))
        # time.sleep(5)
        pass

startTime = datetime.datetime.now()


def buy_stock():
    global purchased_items, balance, purchased_items, buying_times, total_fees_broker, earned_money
    global value_each_purchase, stop_value, risk_ratio, commission_broker, total_fees_broker, stock

    purchased_items = value_each_purchase / price_now
    balance -= value_each_purchase + commission_broker
    buying_times += 1
    total_fees_broker += commission_broker
    earned_money -= commission_broker


def sell_stock():
    global purchased_items, balance, purchased_items, buying_times, total_fees_broker, earned_money
    global value_each_purchase, stop_value, risk_ratio, commission_broker, total_fees_broker, stock
    global value_position_now, winning_sales, loosing_sales

    balance += value_position_now - commission_broker
    earned_money += value_position_now - value_each_purchase - commission_broker
    purchased_items = 0
    if value_position_now > value_each_purchase + commission_broker:
        winning_sales += 1
    else:
        loosing_sales += 1
    total_fees_broker += commission_broker


try:
    # print(df)
    i = 0
    for date in df.index:
        i += 1
        # print(df[date])
        # print(df[date], df['Close'])

        # price_now = get_live_price(STOCK)
        price_date = date
        price_now = df[date]

        # Buying
        if purchased_items <= 0:
            buy_stock()
        value_position_now = purchased_items * price_now
        # Selling
        if value_position_now > (value_each_purchase + (risk_ratio * stop_value)):
            sell_stock()
        elif value_position_now < (value_each_purchase - stop_value):
            sell_stock()
        else:
            pass

        # time.sleep(1)

except KeyboardInterrupt:
    pass
os.system("clear")
print(f"Days runned: {i}\n", end="")
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
