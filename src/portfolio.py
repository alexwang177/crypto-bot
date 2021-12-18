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
