from binance.client import Client
import datetime
import pandas as pd

# YOUR API KEYS HERE
api_key = ""  # Enter your own API-key here
api_secret = ""  # Enter your own API-secret here

bclient = Client(api_key=api_key, api_secret=api_secret)

start_date = datetime.datetime.strptime('1 Dec 2021', '%d %b %Y')
today = datetime.datetime.today()


def binanceBarExtractor(symbol, start_date_str):
    print('working...')

    # start_date_str example: 1 Dec 2021
    start_date = datetime.datetime.strptime(start_date_str, '%d %b %Y')
    today = datetime.datetime.today()

    filename = '{}_MinuteBars.csv'.format(symbol)

    klines = bclient.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE, start_date.strftime(
        "%d %b %Y %H:%M:%S"), today.strftime("%d %b %Y %H:%M:%S"), 1000)
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close',
                                         'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    data.set_index('timestamp', inplace=True)
    data.to_csv(filename)

    print('finished!')


if __name__ == '__main__':
    binanceBarExtractor('BTCUSDT', '1 Dec 2021')
