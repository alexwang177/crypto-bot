'''
    Python script that performs backtesting on our bot
'''

import pandas as pd
from binance.client import Client
import datetime

# YOUR API KEYS HERE
api_key = ""    #Enter your own API-key here
api_secret = "" #Enter your own API-secret here

bclient = Client(api_key=api_key, api_secret=api_secret)

start_date = datetime.datetime.strptime('1 Jan 2016', '%d %b %Y')
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
    df = csv_to_dataframe('BTCUSDT-1m-2021-12-16.csv')

    for i, row in df.iterrows():
        print(row["close"])