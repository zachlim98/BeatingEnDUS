class Trade:
    def __init__(self, id, value, exp):
        self.id = id
        self.value = value
        self.exp = exp

    def update_trade(self, value):
        self.value = value

    def get_value(self):
        return self.value

class AccountBal:
    def __init__(self, value):
        self.value = value
        self.trade_val = []
        self.account_bal = []

    def add_trade(self, trade_val):
        self.trade_val.append(trade_val)

    def update_balance(self, change):
        self.value = self.value + change
        self.account_bal.append(self.value)

class TradeOperations:
    @staticmethod
    def close_trade(account, curr_trade, close_val, next_trade):
        account.add_trade(curr_trade.get_value())
        account.update_balance(curr_trade.get_value() - close_val)
        curr_trade.update_trade(close_val)
        account.add_trade(-curr_trade.get_value())
        account.add_trade(next_trade.get_value())
