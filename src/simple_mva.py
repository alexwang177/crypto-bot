'''
    Class that defines strategy for our crypto-trading bot
'''

from collections import deque
from strategy import Strategy
from action import Action


class SimpleMVA(Strategy):

    def __init__(self, period, equity_per_trade, stop_loss, take_profit):
        # number of time periods in window
        self.period = period
        # percentage of portfolio's value that is used per trade
        self.equity_per_trade = equity_per_trade
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.sum = 0
        self.window = deque()
        self.prev_price = None
        self.buy_orders = []

    def _handle_stop_loss_and_take_profit(self, price):

        actions = []

        for order in self.buy_orders:

            if order.signal == 'BUY' and (price >= order.take_profit_strike or price <= order.stop_loss_strike):

                print('STOP LOSS OR TAKE PROFIT')

                actions.append(Action(signal='SELL',
                                      currency=order.currency,
                                      quantity=order.quantity,
                                      price=price))

            self.buy_orders.remove(order)

        return actions

    def take_action(self, price, port):
        self.window.append(price)
        self.sum += price

        if len(self.window) < self.period:
            return [Action(signal='HOLD', currency=port.get_coin(), quantity=None, price=price)]

        if len(self.window) > self.period:
            self.sum -= self.window.popleft()

        mva = self.sum / self.period

        prev_price = self.prev_price
        self.prev_price = price

        stop_loss_take_profit_actions = self._handle_stop_loss_and_take_profit(
            price)

        # upward trend, price crosses above mva
        if prev_price and prev_price < mva and price > mva:
            buy_action = Action(signal='BUY',
                                currency=port.get_coin(),
                                quantity=self.equity_per_trade *
                                port.get_value_in_coin(coin_price=price),
                                price=price,
                                stop_loss=self.stop_loss,
                                take_profit=self.take_profit)

            self.buy_orders.append(buy_action)
            return stop_loss_take_profit_actions + [buy_action]

        # downward trend, price crosses below mva
        if prev_price and prev_price > mva and price < mva:
            sell_action = Action(signal='SELL',
                                 currency=port.get_coin(),
                                 quantity=self.equity_per_trade *
                                 port.get_value_in_coin(coin_price=price),
                                 price=price)

            return stop_loss_take_profit_actions + [sell_action]

        return stop_loss_take_profit_actions + [Action(signal='HOLD', currency=port.get_coin(), quantity=None, price=price)]

    def get_period(self):
        return self.period

    def get_mva(self):
        return self.sum / self.period if len(self.window) == self.period else None
