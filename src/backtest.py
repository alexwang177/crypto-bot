'''
    Python script that performs backtesting on our bot
'''

import pandas as pd
import matplotlib.pyplot as plt
import os
from simple_mva import SimpleMVA


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


def run_backtest(strat, df):

    start_usd = 1000
    start_btc = start_usd / df['close'][0]

    usd = start_usd
    btc = None

    btc_price = []
    mvas = []
    portfolio = []
    portfolio_hold = []

    for _, row in df.iterrows():
        price = row['close']
        action = strat.take_action(float(price))

        btc_price.append(price)

        mva = strat.get_mva()
        mvas.append(mva)

        if usd and action == 'BUY':
            btc = usd / price
            usd = None
        elif btc and action == 'SELL':
            usd = btc * price
            btc = None

        portfolio_val = usd if usd else btc * price
        portfolio.append(portfolio_val)

        portfolio_hold.append(start_btc * price)

        print(f'price: {price} action: {action}')
        print(f'usd: {usd} btc: {btc} total value (usd): {portfolio_val}')
        print('--------------\n')

    plot_data(x_data=[range(len(btc_price)), range(len(mvas))],
              y_data=[btc_price, mvas],
              labels=['BTC', 'Moving Average'],
              name=f'btc_{strat.get_period()}_period_moving_average.png')

    plot_data(x_data=[range(len(portfolio_hold)), range(len(portfolio))],
              y_data=[portfolio_hold, portfolio],
              labels=['Portfolio Hold', 'Portfolio'],
              name=f'btc_{strat.get_period()}_period_portfolio.png')


if __name__ == '__main__':

    strategies = [SimpleMVA(5), SimpleMVA(10), SimpleMVA(
        20), SimpleMVA(60), SimpleMVA(144), SimpleMVA(1440)]
    df = pd.read_csv('BTCUSDT_MinuteBars.csv')

    for strat in strategies:
        run_backtest(strat, df)
