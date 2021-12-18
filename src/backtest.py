'''
    Python script that performs backtesting on our bot
'''

import pandas as pd
import matplotlib.pyplot as plt
import os
from simple_mva import SimpleMVA
from portfolio import Portfolio


def csv_to_dataframe(filename):
    return pd.read_csv(filename, names=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])


def save_plot(name):
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'backtest_results/')

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.savefig(os.path.join(results_dir, name))


def plot_function(x, y, label):
    plt.plot(x, y, label=label)


def plot_data(x_data, y_data, labels, name):
    plt.figure(figsize=(24, 12))

    for x, y, label in zip(x_data, y_data, labels):
        plt.plot(x, y, label=label)

    plt.ylabel('Price (USD)')
    plt.legend(loc='upper center')

    save_plot(name)
    plt.close()


def run_backtest(strat, port, df):

    # start_fiat = port.get_fiat_quantity()
    # start_coin = start_fiat / df['close'][0]

    # usd = start_usd
    # btc = None

    start_fiat = port.get_fiat_quantity()
    start_coin = start_fiat / df['close'][0]

    coin_price = []
    mvas = []
    portfolio = []
    portfolio_hold = []

    for _, row in df.iterrows():

        # get price of coin
        price = row['close']
        coin_price.append(price)

        # update moving average
        mva = strat.get_mva()
        mvas.append(mva)

        action = strat.take_action(price=float(price), port=port)

        if action.signal == 'BUY' and port.get_fiat_quantity() >= action.quantity * price:
            port.set_fiat_quantity(
                port.get_fiat_quantity() - (action.quantity * price))
            port.set_coin_quantity(
                port.get_coin_quantity() + action.quantity)
        elif action.signal == 'SELL':
            port.set_fiat_quantity(
                port.get_fiat_quantity() + (action.quantity * price))
            port.set_coin_quantity(
                port.get_fiat_quantity() - action.quantity
            )

        portfolio.append(port.get_value_in_fiat())
        portfolio_hold.append(start_coin * price)

        print(f'price: {price} action: {action}')
        print(f'{port.get_fiat()}: {port.get_fiat_quantity()} {port.get_coin()}: {port.get_coin_quantity()} total value ({port.get_fiat()}): {port.get_value_in_fiat()}')
        print('--------------\n')

    percent_change = ((portfolio[-1] - start_fiat) / start_fiat) * 100

    plot_data(x_data=[range(len(coin_price)), range(len(mvas))],
              y_data=[coin_price, mvas],
              labels=[port.get_coin(), 'Moving Average'],
              name=f'{port.get_coin()}_{strat.get_period()}_period_moving_average.png')

    plot_data(x_data=[range(len(portfolio_hold)), range(len(portfolio))],
              y_data=[portfolio_hold, portfolio],
              labels=['Portfolio Hold', 'Portfolio'],
              name=f'{port.get_coin()}_{strat.get_period()}_period_portfolio.png')

    file = open(
        f'backtest_results/{port.get_coin()}_{strat.get_period()}_summary.txt', 'w+')
    file.write(f'Starting {port.get_fiat()}: {start_fiat}\n')
    file.write(f'Ending {port.get_fiat()}: {portfolio[-1]}\n')
    file.write(f'Ending {port.get_fiat()} if hold: {portfolio_hold[-1]}\n')
    file.write(f'Change: {percent_change} %\n')


if __name__ == '__main__':

    # Goal: user can enter any pair of currencies, for example BTC - USD, and the script will run all the specified backtests

    strategies = [SimpleMVA(period=5, equity_per_trade=0.20),
                  SimpleMVA(period=10, equity_per_trade=0.20),
                  SimpleMVA(period=20, equity_per_trade=0.20),
                  SimpleMVA(period=60, equity_per_trade=0.20),
                  SimpleMVA(period=144, equity_per_trade=0.20),
                  SimpleMVA(period=1440, equity_per_trade=0.20)]

    portfolios = [Portfolio(coin='BTC', coin_quantity=0,
                            fiat='USD', fiat_quantity=100),
                  Portfolio(coin='BTC', coin_quantity=0,
                            fiat='USD', fiat_quantity=100),
                  Portfolio(coin='BTC', coin_quantity=0,
                            fiat='USD', fiat_quantity=100),
                  Portfolio(coin='BTC', coin_quantity=0,
                            fiat='USD', fiat_quantity=100),
                  Portfolio(coin='BTC', coin_quantity=0,
                            fiat='USD', fiat_quantity=100),
                  Portfolio(coin='BTC', coin_quantity=0,
                            fiat='USD', fiat_quantity=100)]

    df = pd.read_csv('BTCUSDT_MinuteBars.csv')

    for strat, port in zip(strategies, portfolios):
        run_backtest(strat, port, df)
