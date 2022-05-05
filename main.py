from pydoc import cli
from queue import PriorityQueue
from numpy import absolute

from sympy import symbols
from Lincrum.BinanceClient import BinanceClient
from datetime import datetime
from typing import List, Dict
import pandas as pd
import math
import decimal
import numpy as np
from binance.binanceConstants import *


def main():
    # DEMO
    # api_key = 'aw7d5RzyRHlwjFPrEUlSzz2zYs8Lf3Q5cxkvcYkFmKrWYR6hWUYNLNepAWksEgSw'
    # api_secret = 'yPPUJybVEhg2oInP2xYWHISMDI6hCWyFfN0oWwKnVYPtag01CDLMc8BysrKlrbrO'
    # client = BinanceClient(api_key, api_secret, 'DEMO', PriorityQueue())
    # REAL
    api_key = 'aw7d5RzyRHlwjFPrEUlSzz2zYs8Lf3Q5cxkvcYkFmKrWYR6hWUYNLNepAWksEgSw'
    api_secret = 'yPPUJybVEhg2oInP2xYWHISMDI6hCWyFfN0oWwKnVYPtag01CDLMc8BysrKlrbrO'
    client = BinanceClient(api_key, api_secret, 'REAL', PriorityQueue())

    symbols = pd.DataFrame(client.getAllSymbols())
    symbols = symbols[symbols[0].str.contains('USDT')]
    print(symbols)
    begin_date = int(round(datetime.timestamp(datetime.strptime('05/05/22 00:00:01', '%d/%m/%y %H:%M:%S'))))
    now_date = int(round(datetime.timestamp(datetime.now())))
    print(start_date, end_date)

    for symbol in symbols[0]:
        start_date = begin_date
        end_date = start_date - 999
        coin_klines = []
        for _ in np.arange(now_date, begin_date, -999):
            klines = client.getKlinesBetweenDates(symbol, KLINE_INTERVAL_1MINUTE, start_date, end_date, limit=1000)
            print(symbol)
            print('START DATE = ', str(datetime.fromtimestamp(klines[0][0] / 1000.0)))
            print('END DATE = ', str(datetime.fromtimestamp(klines[-1][0] / 1000.0)))
            coin_klines.append(klines)
            if end_date - 1000 < begin_date:
                end_date = begin_date
            else:
                start_date = end_date - 1
                end_date = end_date - 1000

        df = pd.concat(coin_klines)
        columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades',
                   'Taker buy base asset volume', 'Taker buy qoute asset volume', 'Ignore']
        df.columns = columns
        df.reset_index(drop=True, inplace=True)
        df.drop(columns='Ignore', inplace=True)
        file_name = symbol + '_' + KLINE_INTERVAL_1MINUTE + '.csv'
        df.to_csv(file_name)

    df = pd.DataFrame(client.getKlinesBetweenDates('BTCUSDT', '1m', '01-01-2010', '04-05-2022', limit=1000))

    print(df)
    # client.openPosition('BTCUSDT', pos_quantity=0.001)
    # client.openBuyLimitPosition('BTCUSDT', pos_quantity=0.1, pos_price = 10000)
    # client.getRecentKline('BTCUSDT')
    # all_orders:List[List[Dict]] = client.getAllOrders()
    # last_orders =[]
    # for orders in all_orders:
    #     last_orders.append(max(orders, key=lambda x: x['updateTime']))
    # print(last_orders)
    # res = client.exchangeInfo('BTCUSDT')
    # filters = res['symbols'][0]['filters']
    # percent_price = [x for x in filters if x['filterType'] == 'PERCENT_PRICE'][0]
    # multiplier_up = float(percent_price['multiplierUp'])
    # multiplier_down = float(percent_price['multiplierDown'])

    # price = float(client.getTickerPrice('BTCUSDT')['price'])
    # print(multiplier_down*price)
    # print(multiplier_up*price)#
    # res = client.getLastKlines('BTCUSDT', '1m', 10)
    # df = pd.DataFrame(res)
    # print(df)
    # df = df[[0,1,2,3,4,5]]

    # df.rename(columns={0:'open_time', 1:'open', 2:'high', 3:'low', 4:'close', 5:'volume', 6:'close_time', 7:'quote_asset_volume', 8:'number_of_trades', 9:'base_asset_volume', 10:'quote_asset_volume', 11:'ignore'}, inplace=True)
    # df.rename(columns={0:'timestamp',1:'open', 2:'high', 3:'low', 4:'close', 5:'volume'}, inplace=True)
    # df.set_index = pd.to_datetime(df['timestamp'],unit='ms')
    # df.drop('timestamp', inplace=True, axis=1)
    # print(df)
    # orders = client.getAllOrders()
    # print(orders)
    # client.getOrderStatus('BTCUSDT', 7431523)
    # client.exchangeInfo()
    # client.openBuyLimitPosition('ETHUSDT', 0.1, 2900.0)
    # client.closeOrder('BTCUSDT', orderId = 7431523)
    # client.openSellLimitPosition('BTCUSDT', 0.1, 55000)
    # print(pd.DataFrame(client.getAllOrders())[['symbol', 'orderId', 'status', 'price','origQty', 'cummulativeQuoteQty', 'type', 'side']])
    # print(pd.DataFrame(client.accountStatus()['balances']))
    # print(client.getOrderStatus('BTCUSDT', 7431523))
    # client.closePosition('ETHUSDT', quantity=1)
    # client.openPosition('ETHUSDT', pos_quantity=1, price = 3500)
    # open = client.getOpenOrders()
    # allOrders = client.getAllOrders()
    # for o in open:
    #     if o in allOrders:
    #         print('True')
    #         print(o)
    # res = client.getMyTrades(['BTCUSDT'])
    # print(res[0][-1])
    # client.openSellLimitPosition('BTCUSDT', 0.1, 50000)
    # acc = client.accountStatus()
    # acc = [x for x in acc['balances'] if float(x['free']) > 0.0]
    # print(acc)
    # print(pd.DataFrame(client.getAllOrders()).sort_values(by=['time'])[['symbol', 'orderId', 'status', 'price','origQty', 'cummulativeQuoteQty', 'type', 'side', 'time']])
    # print(pd.DataFrame(client.accountStatus()['balances']))
    # client.getTickerPrice('BTCUSDT')
    # res = client.accountStatus()
    # acc = [x for x in res['balances'] if float(x['free']) > 0.0 or float(x['locked']) > 0.0]
    # for a in acc:
    #     print(a)
    # client.accountStatus()
    # client.getRecentKline('XRPBTC')
    # symbol': 'BNBBTC', 'quantity': '220235.94'
    #res = client.exchangeInfo('BNBBTC')
    #client.openBuyLimitPosition('XRPBTC', 125000000, round(1.5258532482252583e-05, 8))
    # client.getOpenOrders()
    # res = client.getAllOrders()
    # print(res)
    # client.getTickerPrice('BNBBTC')
    # res = client.exchangeInfo('TRXUSDT')
    # prec = res['symbols'][0]['filters']
    # print()
    # print(prec)
    # print()
    # lot_size = [x for x in prec if x['filterType'] == 'LOT_SIZE'][0]
    # print()
    # print(lot_size)

    # step_size = lot_size['stepSize']
    # print()
    # print(step_size)
    # print(str(float(step_size)))
    # print()
    # prec = str(float(step_size))[::-1].find('.')
    # print('PREC')
    # print(float(prec))
    # prec = '0.00000000'[::-1].find('.')
    # print(prec)
    # if float(prec) < 0:
    #     prec = str(float(step_size) * 10000)[::-1].find('.') + 4
    #     print('123')
    # elif float(prec) == 1.0:
    #     print('DUPA')
    #     prec = 8
    # form = '.' + str(prec) + 'f'
    # print(form)
    # print(prec)
    # print(format(6813.69993405, form))
    #client.openPosition('ETHBTC', 1000.0)
    # client.exchangeInfo('BNBBTC')
    #print(format(0.35273952, '.f'))
    # print(client.getAllOrders())

    #client.openPosition('XRPUSDT', 2409.75636945)
    # print(pd.DataFrame(client.bookTicker()))
    # client.accountStatus()
    # client.bookTicker('TRXUSDT')
    #client.openPosition('TRXUSDT', 1.6)
    # client.accountStatus()


if __name__ == "__main__":
    main()
