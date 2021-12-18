class Action:

    def __init__(self, type, currency, quantity, stop_loss=None, take_profit=None):
        self.type = type
        self.currency = currency
        self.quantity = quantity
        self.stoploss = stop_loss
        self.take_profit = take_profit

    def get_type(self):
        return self.type

    def get_currency(self):
        return self.currency

    def get_quantity(self):
        return self.quantity
