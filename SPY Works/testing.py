from fuctions import Trade, AccountBal
from datetime import timedelta
from datetime import date
import pandas as pd
import glob

# truncated = pd.read_pickle("truncated.pickle")

curr_trade = Trade("SPY2019-06-10P288", 3.40, date(2019,6,10))
next_trade = Trade("SPY2019-06-17P290", 2.40, date(2019,6,17))
my_account = AccountBal(100)

my_account.add_trade(curr_trade.get_value())
print(my_account.trade_val)

