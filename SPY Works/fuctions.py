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

    def add_trade(self, trade_val):
        self.trade_val.append(trade_val)

    def update_balance(self, change):
        self.value = self.value + change