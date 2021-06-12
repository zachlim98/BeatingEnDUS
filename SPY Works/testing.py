from fuctions import Trade, AccountBal, TradeOperations
from datetime import timedelta
from datetime import date
import pandas as pd

# truncated = pd.read_pickle("truncated.pickle")

curr_trade = Trade("SPY2019-06-10P288", 3.40, date(2019, 6, 10))
my_account = AccountBal(100)
next_trade = Trade("SPY2019-06-17P290", 2.40, date(2019, 6, 17))
TradeOperations.close_trade(my_account, curr_trade, 0.40, next_trade)
curr_trade = next_trade

print(my_account.trade_val)
print(my_account.account_bal)
