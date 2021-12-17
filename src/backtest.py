'''
    Python script that performs backtesting on our bot
'''

import pandas as pd
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

    strat = Strategy(144)
    df = pd.read_csv('BTCUSDT_MinuteBars.csv')
    usd = 10**9
    btc = None

    for i, row in df.iterrows():
        price = row["close"]
        action = strat.take_action(float(price))

        
        if usd and action == 'BUY':
            btc = usd / price
            usd = None
        elif btc and action == 'SELL':
            usd = btc * price
            btc = None
        
        print(f"price: {price} action: {action}")
        print(f"usd: {usd} btc: {btc} total value (usd): {usd if usd else btc * price}")
        print("--------------\n")

