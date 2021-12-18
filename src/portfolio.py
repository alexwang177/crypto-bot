'''
    Class that defines Portfolio
'''


class Portfolio:

    def __init__(self, coin, coin_quantity, fiat, fiat_quantity):
        self.coin = coin
        self.coin_quantity = coin_quantity
        self.fiat = fiat
        self.fiat_quantity = fiat_quantity
        self.orders = []

    def get_coin(self):
        return self.coin

    def get_coin_quantity(self):
        return self.coin_quantity

    def get_fiat(self):
        return self.fiat

    def get_fiat_quantity(self):
        return self.fiat_quantity

    def get_value_in_fiat(self, coin_price):
        return self.fiat_quantity + (self.coin_quantity * coin_price)

    def get_value_in_coin(self, coin_price):
        return self.coin_quantity + (self.fiat_quantity / coin_price)

    def set_coin_quantity(self, new_coin_quantity):
        self.coin_quantity = new_coin_quantity

    def set_fiat_quantity(self, new_fiat_quantity):
        self.fiat_quantity = new_fiat_quantity

    def handle_action(self, action):
        if action.signal == 'BUY' and self.get_fiat_quantity() >= action.quantity * action.price:
            self.set_fiat_quantity(
                self.get_fiat_quantity() - (action.quantity * action.price))
            self.set_coin_quantity(
                self.get_coin_quantity() + action.quantity)
        elif action.signal == 'SELL' and self.get_coin_quantity() >= action.quantity:
            self.set_fiat_quantity(
                self.get_fiat_quantity() + (action.quantity * action.price))
            self.set_coin_quantity(
                self.get_coin_quantity() - action.quantity
            )
