'''
    Class that defines strategy for our crypto-trading bot
'''

from collections import deque
from strategy import Strategy
from action import Action


class SimpleMVA(Strategy):

    def __init__(self, period, equity_per_trade):
        # number of time periods in window
        self.period = period
        # percentage of portfolio's value that is used per trade
        self.equity_per_trade = equity_per_trade
        self.sum = 0
        self.window = deque()
        self.prev_price = None

    def take_action(self, price, port):
        self.window.append(price)
        self.sum += price

        if len(self.window) < self.period:
            return Action('HOLD', port.get_coin(), None)

        if len(self.window) > self.period:
            self.sum -= self.window.popleft()

        mva = self.sum / self.period

        prev_price = self.prev_price
        self.prev_price = price

        # upward trend, price crosses above mva
        if prev_price and prev_price < mva and price > mva:
            return Action('BUY',
                          port.get_coin(),
                          self.equity_per_trade *
                          port.get_value_in_coin(coin_price=price),
                          stop_loss=0.03,
                          take_profit=0.06)

        # downward trend, price crosses below mva
        if prev_price and prev_price > mva and price < mva:
            return Action('SELL',
                          port.get_coin(),
                          self.equity_per_trade *
                          port.get_value_in_coin(coin_price=price),
                          stop_loss=0.03,
                          take_profit=0.06)

        return Action('HOLD', port.get_coin(), None)

    def get_period(self):
        return self.period

    def get_mva(self):
        return self.sum / self.period if len(self.window) == self.period else None
