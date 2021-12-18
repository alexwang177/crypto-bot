class Order:

    def __init__(self, type, currency, quantity, stop_loss=0.03, take_profit=0.06):
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
