class Action:

    def __init__(self, signal, currency, quantity, price, stop_loss=None, take_profit=None):
        self.signal = signal
        self.currency = currency
        self.quantity = quantity
        self.price = price
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        if stop_loss:
            self.stop_loss_strike = (1.00 - stop_loss) * self.price

        if take_profit:
            self.take_profit_strike = (1.00 + take_profit) * self.price

    def get_type(self):
        return self.type

    def get_currency(self):
        return self.currency

    def get_quantity(self):
        return self.quantity
