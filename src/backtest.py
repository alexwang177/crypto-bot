'''
    Python script that performs backtesting on our bot
'''

import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client
import datetime
from strategy import Strategy

# YOUR API KEYS HERE
api_key = ""    #Enter your own API-key here
api_secret = "" #Enter your own API-secret here

bclient = Client(api_key=api_key, api_secret=api_secret)

start_date = datetime.datetime.strptime('1 Dec 2021', '%d %b %Y')
today = datetime.datetime.today()

def binanceBarExtractor(symbol):
    print('working...')
    filename = '{}_MinuteBars.csv'.format(symbol)

    klines = bclient.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, start_date.strftime("%d %b %Y %H:%M:%S"), today.strftime("%d %b %Y %H:%M:%S"), 1000)
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    data.set_index('timestamp', inplace=True)
    data.to_csv(filename)
    print('finished!')

def csv_to_dataframe(filename):
    return pd.read_csv(filename, names=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])

if __name__ == '__main__':

    strat = Strategy(20)
    df = pd.read_csv('BTCUSDT_MinuteBars.csv')

    start_usd = 10**9
    start_btc = start_usd / df["close"][0]

    usd = start_usd
    btc = None

    btc_price = []
    mvas = []
    portfolio = []
    portfolio_hold = []

    for i, row in df.iterrows():
        price = row["close"]
        action = strat.take_action(float(price))

        btc_price.append(price)
        mvas.append(strat.get_mva())
        
        if usd and action == 'BUY':
            btc = usd / price
            usd = None
        elif btc and action == 'SELL':
            usd = btc * price
            btc = None

        portfolio_val = usd if usd else btc * price
        portfolio.append(portfolio_val)

        portfolio_hold.append(start_btc * price)
        
        print(f"price: {price} action: {action}")
        print(f"usd: {usd} btc: {btc} total value (usd): {portfolio_val}")
        print("--------------\n")

    plt.figure(figsize=(24, 12))
    plt.plot(range(len(btc_price)), btc_price, label="BTC")
    plt.plot(range(len(mvas)), mvas, label="Moving Average")
    plt.ylabel("Price (USD)")
    plt.legend(loc='upper center')
    plt.savefig(f'btc_{strat.get_period()}_period_moving_average.png')

    plt.close()
    
    plt.figure(figsize=(24, 12))
    plt.plot(range(len(portfolio_hold)), portfolio_hold, label="Portfolio Hold")
    plt.plot(range(len(portfolio)), portfolio, label="Portfolio")
    plt.ylabel("Price (USD)")
    plt.legend(loc='upper center')
    plt.savefig(f'btc_{strat.get_period()}_period_portfolio.png')
