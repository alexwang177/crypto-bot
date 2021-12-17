'''
    Class that defines strategy for our crypto-trading bot
'''

from collections import deque
from strategy import Strategy


class SimpleMVA(Strategy):

    def __init__(self, period):
        self.period = period  # number of time periods in window
        self.sum = 0
        self.window = deque()
        self.prev_price = None

    def take_action(self, price):
        self.window.append(price)
        self.sum += price

        if len(self.window) < self.period:
            return "HOLD"

        if len(self.window) > self.period:
            self.sum -= self.window.popleft()

        mva = self.sum / self.period

        prev_price = self.prev_price
        self.prev_price = price

        # upward trend, price crosses above mva
        if prev_price and prev_price < mva and price > mva:
            return "BUY"

        # downward trend, price crosses below mva
        if prev_price and prev_price > mva and price < mva:
            return "SELL"

        return "HOLD"

    def get_period(self):
        return self.period

    def get_mva(self):
        return self.sum / self.period if len(self.window) == self.period else None
