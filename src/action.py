class Action:

    def __init__(self, signal, currency, quantity, price, stop_loss=None, take_profit=None):
        self.signal = signal
        self.currency = currency
        self.quantity = quantity
        self.price = price
        self.stoploss = stop_loss
        self.take_profit = take_profit

    def get_type(self):
        return self.type

    def get_currency(self):
        return self.currency

    def get_quantity(self):
        return self.quantity
