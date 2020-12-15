get_ipython().run_line_magic("matplotlib", " inline")

from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf
import tulipy as ta
import matplotlib.pyplot as plt
import tiingo
import pandas as pd 
import pyfolio as pf
import math
import numpy as np


class QuantConnectCSVData(btfeeds.GenericCSVData):

    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', 'get_ipython().run_line_magic("Y:%m:%d'),", "")
        ('datetime', 0),
        ('time', 1),
        ('open', 2),
        ('high', 3),
        ('low', 4),
        ('close', 5),
        ('volume', 6),
        ('openinterest', -1),
        ('timeframe', bt.TimeFrame.Minutes), 
        ('compression', 240),
    )


class TiingoCSVData(btfeeds.GenericCSVData):
    lines = ('inSPY',)
    
    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', 'get_ipython().run_line_magic("Y-%m-%d'),", "")
        ('datetime', 0),
        ('open', 9),
        ('high', 7),
        ('low', 8),
        ('close', 6),
        ('volume', 10),
        ('inSPY', 13),
        ('openinterest', -1),
    )


class RSIt(bt.Strategy):

    params = (('oneplot', True),
                ('tp_multiplier', 5),
                ('sl_multiplier', 3),
                ('ATR_Period', 14),
                ('bk_period', 100),
                )

    def __init__(self):
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[i] = dict()
            self.inds[i]['ATR']= bt.indicators.AverageTrueRange(d, period=self.p.ATR_Period)
            self.inds[i]['bkhigh'] = bt.indicators.Highest(d,period=self.p.bk_period)
            self.inds[i]['bklow'] = bt.indicators.Lowest(d, period=self.p.bk_period)

            if i > 0:
                if self.p.oneplot == True:
                    d.plotinfo.plotmaster = self.datas[0]

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size
            cash = self.broker.getcash()
            dt = self.data.datetime.date()
            if not pos:  # no market / no orders
                if (d.close[0] get_ipython().getoutput("= 0) and (d.inSPY[0] == 1):")
                    if (d.close[0] > self.inds[i]['bkhigh'][-1]):
                        # self.buy(data=d, size=100)                    
                        price = d.close[0]
                        price_limit = price + (self.p.tp_multiplier*self.inds[i]['ATR'][0])
                        price_stop = price - (self.p.sl_multiplier*self.inds[i]['ATR'][0])
                        qty = round((cash*0.01)/(price - price_stop))

                        if qty get_ipython().getoutput("= 0:    ")
                            self.buy_bracket(
                                data=d,
                                size=qty,
                                exectype=bt.Order.Market,
                                limitprice=price_limit,
                                price=price,
                                stopprice=price_stop,
                                )

                    elif (d.close[0] < self.inds[i]['bklow'][-1]):
                        # self.sell(data=d, size=100)

                        price = d.close[0]
                        price_limit = price - (self.p.tp_multiplier*self.inds[i]['ATR'][0])
                        price_stop = price + (self.p.sl_multiplier*self.inds[i]['ATR'][0])
                        qty = round((cash*0.01)/(price_stop - price))

                        if qty get_ipython().getoutput("= 0: ")
                            self.sell_bracket(
                                    data=d,
                                    price=price,
                                    size=qty,
                                    exectype=bt.Order.Market,
                                    stopprice=price_stop,
                                    limitprice=price_limit,
                                )
                else:
                    pass
            
            elif pos:
                pass
    

#         def stop(self):
#             print('LB Params: {} End value: {}'.format(self.p.bk_period, self.broker.getvalue()))
                
    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        if trade.isclosed:
            print('{} {} Closed: PnL Gross {}, Net {}, Cash left {:.2f}'.format(
                                                dt,
                                                trade.data._name,
                                                round(trade.pnl,2),
                                                round(trade.pnlcomm,2),
                                                self.broker.getcash()))


a


class Momentum(bt.Indicator):
    lines = ('pctreturn',)
    params = (('period', 12),)
    
    def __init__(self):
        self.addminperiod(self.params.period)
    
    def next(self):
        a = (self.data.get(ago=0, size=(self.p.period+1)))
        df = pd.DataFrame(a)
#         df_change = ((df.pct_change()+1).cumprod())-1
        df_changes = (df.pct_change()).mean()
        self.lines.pctreturn[0] = df_changes*100


class Test(bt.Strategy):
    
    params = (('period', 12),
            )
    
    def __init__(self):
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[i] = dict()
            self.inds[i]['Momen']= Momentum(d, period=self.p.period)

    def next(self):
        dt = self.data.datetime.date()
        for i,d in enumerate(self.datas):
            print('Ticker: {} Time: {}, Price: {:2f}, and Returns: {:.4f}'.format(d._name, dt, d.close[0], self.inds[i]['Momen'][0]))


class TestStrat(bt.Strategy):
    
    params = (('text', 1),
              ('period', 12),
            )
    
    def __init__(self):
        self.i = 0
        self.inds = dict()
        self.spy = self.datas[0]
        self.bil = self.datas[1]
        self.veu = self.datas[2]
        self.agg = self.datas[3]
        self.mospy = Momentum(self.spy, period=self.p.period)
        self.mobil = Momentum(self.bil, period=self.p.period)
        self.moveu = Momentum(self.veu, period=self.p.period)
        self.moagg = Momentum(self.agg, period=self.p.period)
        self.order = None

        
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('get_ipython().run_line_magic("s,", " %s' % (dt.isoformat(), txt))")


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, get_ipython().run_line_magic(".2f'", " % order.executed.price)")
            elif order.issell():
                self.log('SELL EXECUTED, get_ipython().run_line_magic(".2f'", " % order.executed.price)")

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled')
        
        elif order.status in [order.Margin]:
            self.log('Order Margin')
            
        elif order.status in [order.Rejected]:
            self.log('Order Rejected')

        # Write down: no pending order
        self.order = None
        
    def next(self):
        if self.mospy[0] > self.moveu[0]:
            if self.mospy[0] > self.mobil[0]:
                for i in [1,2,3]:
                    self.order = self.order_target_percent(data=self.datas[i], target=0)
                self.order = self.order_target_percent(data=self.datas[0], target=1)
                print('Opening a position of SPY')
                
            else:
                for i in [0,1,2]:
                    self.order = self.order_target_percent(data=self.datas[i], target=0)
                self.order = self.order_target_percent(data=self.datas[3], target=1)
                print('Opening a position of AGG')

        elif self.mospy[0] < self.moveu[0]:
            if self.moveu[0] > self.mobil[0]:
                for i in [0,1,3]:
                    self.order = self.order_target_percent(data=self.datas[i], target=0)
                self.order = self.order_target_percent(data=self.datas[2], target=1)
                print('Opening position of VEU')
            else:
                for i in [0,1,2]:
                    self.order = self.order_target_percent(data=self.datas[i], target=0)
                self.order = self.order_target_percent(data=self.datas[3], target=1)
                print('Opening a position of AGG')


cerebro = bt.Cerebro()

datalist = ["SPY" , "BIL", "VEU", "AGG"]

# Add a strategy
cerebro.addstrategy(TestStrat)
cerebro.addanalyzer(bt.analyzers.PyFolio)

#add datafeeds
for i in range(len(datalist)):
    data = TiingoCSVData(dataname=f'./data/ETFs/{datalist[i]}.csv', fromdate=datetime(2017,1,1),todate=datetime(2020,6,30))
    cerebro.resampledata(data, name=datalist[i], timeframe=bt.TimeFrame.Months)

# Set our desired cash start
cerebro.broker.setcash(100000.0)

# Print out the starting conditions
print('Starting Portfolio Value: get_ipython().run_line_magic(".2f'", " % cerebro.broker.getvalue())")

# Run over everything
strats = cerebro.run()
firstStrat = strats[0]

# Print out the final result
print('Final Portfolio Value: get_ipython().run_line_magic(".2f'", " % cerebro.broker.getvalue())")


import os
path = R'.\data'
files = [os.path.splitext(filename)[0] for filename in os.listdir(path)]


get_ipython().run_line_magic("matplotlib", " inline")


get_ipython().run_line_magic("matplotlib", " widget")

cerebro.plot(iplot=False,style='candle', bardown='yellow', volume=False)


pyfoliozer = firstStrat.analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()


import quantstats as qs

returns_qs = returns.tz_convert(None)
transactions_qs = transactions.tz_convert(None)
positions_qs = positions.tz_convert(None)


qs.reports.full(returns_qs,"SPY")


pf.create_full_tear_sheet(returns=returns,transactions=transactions)


transactions



