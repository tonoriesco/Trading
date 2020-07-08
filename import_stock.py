import pandas_datareader as web

stocks = []
with open("symbols.txt", "r") as f:
    for line in f:
        stocks.append(line.strip())

web.DataReader(stocks, "yahoo", start="2010-1-1")["Adj Close"].to_csv("prices.csv")
web.DataReader(stocks, "yahoo", start="2010-1-1")["Volume"].to_csv("volume.csv")
