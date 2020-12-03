from datetime import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf
import tulipy as ta
import pandas as pd
import matplotlib
import pyfolio

class RSIStrat(bt.Strategy):
    
    def __init__(self):
        self.dataclose= self.datas[0].close    # Keep a reference to the "close" line in the data[0] dataseries
        self.rsi= bt.indicators.RelativeStrengthIndex()
        self.stoch = bt.indicators.Stochastic()
        self.ATR= bt.indicators.AverageTrueRange(period=7)
        self.MAC = bt.indicators.MACDHisto()
        self.order = None # Property to keep track of pending orders.  There are no orders when the strategy is initialized.
        self.buyprice = None
        self.buycomm = None
    
    def log(self, txt, dt=None):
        # Logging function for the strategy.  'txt' is the statement and 'dt' can be used to specify a specific datetime
        dt = dt or self.datas[0].datetime.date(0)
        print('{0},{1}'.format(dt.isoformat(),txt))
    
    def notify_order(self, order):
        # 1. If order is submitted/accepted, do nothing 
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 2. If order is buy/sell executed, report price executed
        if order.status in [order.Completed]: 
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {0:8.2f}, Cost: {1:8.2f}, Comm: {2:8.2f}'.format(
                    order.executed.price,
                    order.executed.value,
                    order.executed.comm))
                
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, {0:8.2f}, Cost: {1:8.2f}, Comm{2:8.2f}'.format(
                    order.executed.price, 
                    order.executed.value,
                    order.executed.comm))
            
            self.bar_executed = len(self) #when was trade executed
        # 3. If order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
            
        self.order = None
    
    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(
            trade.pnl, trade.pnlcomm))
    
    def next(self):
        # Log the closing prices of the series from the reference
        # self.log('Close, {0:8.2f}'.format(self.dataclose[0]))

        if self.order: # check if order is pending, if so, then break out
            return
                
        # since there is no order pending, are we in the market?    
        if not self.position: # not in the market            
            if (self.rsi > 50) and (self.stoch.k > 50) and (self.MAC > 0):
                price = self.dataclose[0]
                price_limit = price + (2.8*self.ATR)
                price_stop = price - (1.2*self.ATR)
                atr_price = self.ATR[0]

                self.order = self.buy_bracket(
                    size=100,
                    price=price,
                    exectype=bt.Order.Market,
                    stopprice=price_stop,
                    limitprice=price_limit,
                )
                self.log('BUY AT: {:8.2f}, Limit: {:8.2f}, Stop: {:8.2f}'.format(price,price_limit,price_stop))

            elif (self.rsi < 50) and (self.MAC < 0) and (self.stoch < 50):
                price = self.dataclose[0]
                price_limit = price - (2.8*self.ATR)
                price_stop = price + (1.2*self.ATR)
                atr_price = self.ATR[0]

                self.order = self.sell_bracket(
                    size=100,
                    price=price,
                    exectype=bt.Order.Market,
                    stopprice=price_stop,
                    limitprice=price_limit,
                )
                self.log('SHORT AT: {:8.2f}, Limit: {:8.2f}, Stop: {:8.2f}'.format(price,price_limit,price_stop))

class RSIt(bt.Strategy):

    params = (('oneplot', True),)

    def __init__(self):
        self.inds = dict()
        self.o = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            self.inds[d]['RSI']= bt.indicators.RelativeStrengthIndex()
            self.inds[d]['stoch'] = (bt.indicators.Stochastic()).k
            self.inds[d]['ATR']= bt.indicators.AverageTrueRange(period=7)
            self.inds[d]['MACD'] = bt.indicators.MACDHisto()

            if i > 0:
                if self.p.oneplot == True:
                    d.plotinfo.plotmaster = self.datas[0]

    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size
            if not pos :  # no market / no orders
                if (self.inds[d]['RSI'][0] > 70) and (self.inds[d]['stoch'][0] > 50) and (self.inds[d]['MACD'][0] > 0):
                    # self.buy(data=d, size=100)                    
                    price = d.close[0]
                    price_limit = price + (1.5*self.inds[d]['ATR'][0])
                    price_stop = price - (1*self.inds[d]['ATR'][0])
                        
                    self.o[d] = self.buy_bracket(
                        data=d,
                        size=100,
                        price=price,
                        exectype=bt.Order.Market,
                        stopprice=price_stop,
                        limitprice=price_limit,
                        )

                elif (self.inds[d]['RSI'][0] < 30) and (self.inds[d]['stoch'][0] < 50) and (self.inds[d]['MACD'][0] < 0):
                    # self.sell(data=d, size=100)

                    price = d.close[0]
                    price_limit = price - (1.5*self.inds[d]['ATR'][0])
                    price_stop = price + (1*self.inds[d]['ATR'][0])
                
                    self.o[d] = self.sell_bracket(
                            data=d,
                            size=100,
                            price=price,
                            exectype=bt.Order.Market,
                            stopprice=price_stop,
                            limitprice=price_limit,
                        )
            
            elif pos:
                pass
            

    def notify_trade(self, trade):
        dt = self.data.datetime.date()
        if trade.isclosed:
            print('{} {} Closed: PnL Gross {}, Net {}'.format(
                                                dt,
                                                trade.data._name,
                                                round(trade.pnl,2),
                                                round(trade.pnlcomm,2)))

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(RSIt)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addanalyzer(bt.analyzers.PyFolio)

    #create our data list
    datalist = ['NFLX','FB','AAPL']

    #Loop through the list adding to cerebro.
    for i in range(len(datalist)):
        data = btfeeds.YahooFinanceData(dataname=datalist[i], fromdate= datetime(2015,1,1), todate= datetime(2020,6,1))
        cerebro.adddata(data, name=datalist[i])

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    strats = cerebro.run()
    strats = strats[0]
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

    pyfolio = strats.analyzers.getbyname('pyfolio')

    returns, positions, transactions, gross_lev = pyfolio.get_pf_items()
