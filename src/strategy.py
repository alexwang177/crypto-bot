'''
    Class that defines strategy for our crypto-trading bot
'''

from collections import deque

class Strategy:

    def __init__(self, period):
        self.period = period # number of time periods in window
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

        # upward trend, price crosses above mva
        if self.prev_price and self.prev_price < mva and price > mva:
            return "BUY"

        # downward trend, price crosses below mva
        if self.prev_price and self.prev_price > mva and price < mva:
            return "SELL"

        return "HOLD"