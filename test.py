# from pandas_datareader import data
from yahoo_fin.stock_info import get_data

# import os

# import sys
import datetime

start_time = datetime.datetime(2010, 7, 1)
# end_time = datetime.datetime(2019, 1, 20)
end_time = datetime.datetime.now().date().isoformat()  # today


connected = 0
while not connected:
    try:
        df = get_data("KO", start_date=start_time, index_as_date=False, interval="1d")
        connected = True
        # print(f"Connected to Yahoo\nGot {df} values\n")
    except Exception as e:
        print("type error: " + str(e))
        # time.sleep(5)
        pass

# for i in range(0, len(df)):
#     print(df.iloc[i]["adjclose"])
# for index, row in df.iterrows():
#     print(row["date"], row["close"])


def fun(num):
    if num < 20:
        return "Low"
    elif num >= 20 and num < 40:
        return "Normal"
    else:
        return "High"


df["Valor"] = df["close"].apply(fun)

print(df)
