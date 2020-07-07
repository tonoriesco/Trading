# optional installations:
# !pip install yfinance --upgrade --no-cache-dir
# !pip3 install pandas_datareader

import sqlite3
import pandas as pd
from pandas_datareader import data
import sys

import datetime
import time

# import yfinance as yf

# pretty printing of pandas dataframe
pd.set_option("expand_frame_repr", False)
# for pandas_datareader, sometimes there can be version mismatch
pd.core.common.is_list_like = pd.api.types.is_list_like

# ___variables___

DBSTOCK = "stock.sqlite3"

STOCK = sys.argv[1]
# Remove the characters that are not nubers and alphabets
# stock_table = re.sub("[\W_]+", "", stock,)
stock_table = STOCK

start_time = datetime.datetime(2010, 1, 1)
# end_time = datetime.datetime(2019, 1, 20)
end_time = datetime.datetime.now().date().isoformat()  # today

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


# use numerical integer index instead of date
df = df.reset_index()

# ___database_part___
engine = sqlite3.connect(DBSTOCK)
cur = engine.cursor()

# data frame to database, table name of stock (ticker)
df.to_sql(stock_table, con=engine, if_exists="replace", index=True)

print(" ")

select_statement = f"SELECT * FROM '{stock_table}' ORDER BY Date DESC LIMIT 10;"
cur.execute(select_statement)
for line in cur.fetchall():
    print(line)
