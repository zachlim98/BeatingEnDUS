import pandas as pd
from tiingo import TiingoClient
from ta.momentum import RSIIndicator, stoch
from ta.trend import MACD as md
from ta.volatility import AverageTrueRange as atr
import numpy as np


client = TiingoClient({'api_key' : '7fb8e25ac6335f846ae82d3f3a28ed535f313592'})

df = pd.read_csv(R"X:\GitHub\beatingENd\BeatingEnDUS\Own Screener\IBD50.csv")

# datalist = (df['Ticker'].to_list())
datalist = ['NFLX', 'AAPL', 'GOOG']

data = client.get_dataframe(datalist,
                                    metric_name='adjClose',
                                      frequency='daily',
                                      startDate='2015-02-02',
                                      endDate='2020-10-10')


nflx_month_ret = data["NFLX"].resample('M').ffill().pct_change().to_frame()


nflx_month_ret["1pRet"] = (nflx_month_ret["NFLX"]+1)
nflx_month_ret["Momentum"] = (nflx_month_ret.iloc[:,1].rolling(12).agg(np.product) - 1)

nflx_month_ret.head(24)


def RSI_base(data,ticker):
    MACD = md(close=data[ticker])
    data["MACD_diff"] = MACD.macd_diff()
    RSI = RSIIndicator(close=data[ticker])
    data["RSI"] = RSI.rsi()
    data["Buy_Signal"] = 0
    data["Pos"] = 0
    data["Sell_Signal"] = 0
    data["SL"] = 0 
    data["TP"] = 0
    data["TW"] = 0.0

    data = data.dropna()

    for i in range(1,len(data)):
        if data["Pos"][i-1] == 0:
            if data["RSI"].iloc[i-1] > 50 and data["MACD_diff"][i-1] > 0 and (data["Pos"][i] == 0):
                data["Buy_Signal"][i] = 1
                data["Pos"][i] = 1
                data["SL"][i] = (data[ticker][i]*0.97)
                data["TP"][i] = (data[ticker][i]*1.5)
            elif data["RSI"].iloc[i-1] < 50 and data["MACD_diff"][i-1] < 0 and (data["Pos"][i] == 0): 
                data["Buy_Signal"][i] = 1
                data["Pos"][i] = -1
                data["SL"][i] = (data[ticker][i]*1.03)
                data["TP"][i] = (data[ticker][i]*0.95)
            else:
                data["Buy_Signal"][i] = 0 
                data["Pos"][i] = 0

        elif data["Pos"][i-1] == 1:
            data["SL"][i] = data["SL"][i-1] 
            data["TP"][i] = data["TP"][i-1]
            if (data[ticker][i-1] > data["SL"][i-1]) or (data[ticker][i-1] < data["TP"][i-1]):
                data["Pos"][i] = 1
            if (data[ticker][i-1] < data["SL"][i-1]) or (data[ticker][i-1] > data["TP"][i-1]):
                data["Pos"][i] = 0
                data["Sell_Signal"][i] = 1

        elif data["Pos"][i-1] == -1:
            data["SL"][i] = data["SL"][i-1] 
            data["TP"][i] = data["TP"][i-1]
            if (data[ticker][i-1] < data["SL"][i-1]) or (data[ticker][i-1] > data["TP"][i-1]):
                data["Pos"][i] = -1
            if (data[ticker][i-1] > data["SL"][i-1]) or (data[ticker][i-1] < data["TP"][i-1]):
                data["Pos"][i] = 0
                data["Sell_Signal"][i] = 1

    for i in range(len(data)):
        if (data["Pos"][i] == 1): 
            data["TW"][i] = 1/len(datalist)
        elif (data["Pos"][i] == -1):
            data["TW"][i] = -(1/len(datalist))
        else:
            data["TW"][i] = 0

    chumps = data["TW"]

    return chumps


def LA_RSI_base(data,ticker):
    MACD = md(close=data[ticker])
    data["MACD_diff"] = MACD.macd_diff()
    RSI = RSIIndicator(close=data[ticker])
    data["RSI"] = RSI.rsi()
    data["Buy_Signal"] = 0
    data["Pos"] = 0
    data["Sell_Signal"] = 0
    data["SL"] = 0 
    data["TP"] = 0
    data["TW"] = 0.0

    data = data.dropna()

    for i in range(0,len(data)):
        if data["Pos"][i-1] == 0:
            if data["RSI"].iloc[i] > 50 and data["MACD_diff"][i] > 0 and (data["Pos"][i] == 0):
                data["Buy_Signal"][i] = 1
                data["Pos"][i] = 1
                data["SL"][i] = (data[ticker][i]*0.97)
                data["TP"][i] = (data[ticker][i]*1.5)
            elif data["RSI"].iloc[i] < 50 and data["MACD_diff"][i] < 0 and (data["Pos"][i] == 0): 
                data["Buy_Signal"][i] = 1
                data["Pos"][i] = -1
                data["SL"][i] = (data[ticker][i]*1.03)
                data["TP"][i] = (data[ticker][i]*0.95)
            else:
                data["Buy_Signal"][i] = 0 
                data["Pos"][i] = 0

        elif data["Pos"][i-1] == 1:
            data["SL"][i] = data["SL"][i-1] 
            data["TP"][i] = data["TP"][i-1]
            if (data[ticker][i] > data["SL"][i]) or (data[ticker][i] < data["TP"][i]):
                data["Pos"][i] = 1
            if (data[ticker][i] < data["SL"][i]) or (data[ticker][i] > data["TP"][i]):
                data["Pos"][i] = 0
                data["Sell_Signal"][i] = 1

        elif data["Pos"][i-1] == -1:
            data["SL"][i] = data["SL"][i-1] 
            data["TP"][i] = data["TP"][i-1]
            if (data[ticker][i] < data["SL"][i]) or (data[ticker][i] > data["TP"][i]):
                data["Pos"][i] = -1
            if (data[ticker][i] > data["SL"][i]) or (data[ticker][i] < data["TP"][i]):
                data["Pos"][i] = 0
                data["Sell_Signal"][i] = 1

    for i in range(len(data)):
        if (data["Pos"][i] == 1): 
            data["TW"][i] = 1/len(datalist)
        elif (data["Pos"][i] == -1):
            data["TW"][i] = -(1/len(datalist))
        else:
            data["TW"][i] = 0

    chumps = data["TW"]

    return chumps


non = LA_RSI_base(data,"AAPL")


nont = RSI_base(data,"AAPL")
nont.to_csv("nont.csv")


df = pd.DataFrame()

for i in datalist:
    temp = RSI_base(data,i)
    temp = temp.rename(i)
    df = pd.concat([df,temp],axis=1)

La_df = pd.DataFrame()

for i in datalist:
    LA_temp = LA_RSI_base(data,i)
    LA_temp = LA_temp.rename(i)
    La_df = pd.concat([La_df,LA_temp],axis=1)


non.to_csv("non.csv")


import bt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ffn as ffn

get_ipython().run_line_magic("matplotlib", " inline")


data = data[['NFLX', 'AAPL', 'GOOG']]


crosses = bt.Strategy('Test1', [bt.algos.WeighTarget(df),
                                    bt.algos.Rebalance()])


crosses_LA = bt.Strategy('LA_noCom', [bt.algos.WeighTarget(La_df),
                                    bt.algos.Rebalance()])

long_only = bt.Strategy('Benchmark', [bt.algos.RunOnce(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighEqually(),
                        bt.algos.Rebalance()])

t = bt.Backtest(crosses,data,commissions=lambda q, p: max(1, abs(q) * 0.05))
nt = bt.Backtest(crosses_LA,data,commissions=lambda q, p: max(1, abs(q) * 0.05))
s = bt.Backtest(long_only, data,commissions=lambda q, p: max(1, abs(q) * 0.05))


report = bt.run(t,nt,s)
report.plot()
plt.title("Portfolio Returns")
plt.savefig("arg.png")

report.display()


Returns = report.prices.to_returns()
Test1_returns = (Returns["Test1"]).tz_convert(None)
Benchmark = Returns["Benchmark"].tz_convert(None)


import quantstats as qs


t.positions.to_clipboard()


nt.positions


a1 = np.array([90.03, 102.57, 91.48, 91.25, 97.45, 98.55, 124.87, 117.0, 123.8, 140.71, 142.13, 147.81, 152.2, 163.07, 150.09])


a = np.array([102.57, 91.48, 91.25, 97.45, 98.55, 124.87, 117.0, 123.8, 140.71, 142.13, 147.81, 152.2, 163.07])


df = pd.DataFrame(a)
df_change = ((df.pct_change()+1).rolling(12).agg(np.product))-1
df_change.iloc[12]
# print(df_change)

# nflx_month_ret["1pRet"] = (nflx_month_ret["NFLX"]+1)
# nflx_month_ret["Momentum"] = (nflx_month_ret.iloc[:,1].rolling(12).agg(np.product) - 1)

# nflx_month_ret


df_changes = (df.pct_change()).rolling(12).mean()


df_changes.iloc[-1]


df_changes


df.pct_change()



