from datetime import date, datetime
from queue import PriorityQueue
from time import sleep
from typing import Dict
from unittest import result

from sympy import symbols
import binance
import logging
from binance.lib.utils import config_logging
from binance.spot import Spot as Client
from binance.binanceConstants import *
from binance.spot.market import exchange_info



DEBUG = False

# connection addresses
REAL_BAPI_ADDRESSES = ['https://api.binance.com', 'https://api1.binance.com', 'https://api2.binance.com', 'https://api3.binance.com']
DEMO_BAPI_ADDRESS = ['https://testnet.binance.vision']

# API inter-command timestamp (in ms)
TIMESTAMP = 200

#Binance constants


# logger properties
logger = logging.getLogger()

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.CRITICAL)
    

config_logging(logging, logging.DEBUG)  
    
class BinanceClient():
    def __init__(self,key,secret,account_type, events_queue:PriorityQueue, encrypt=True):
        self.events_queue = events_queue
        self.address = []
        if account_type=='REAL':
            self.address = REAL_BAPI_ADDRESSES
        else:
            self.address = DEMO_BAPI_ADDRESS
        self.key = key
        self.secret = secret
        self.client = self.login()
        
        
    def login(self):
        for address in self.address:
            try:
                print(address)
                client = Client(self.key, self.secret, base_url=address)
                print('Succesfull login')
                return client
            except Exception:
                print(f"Cannot connect to {address}")
                #self.events_queue.put_nowait((0, ErrorEvent(f"Cannot connect to {address}")))
                
    
    def ping(self):
        return self.client.ping()
    
    
    def serverTime(self):
        return self.client.time()
    
    
    def systemStatus(self):
        return self.client.system_status()
    
    
    def savingAccounts(self):
        return self.client.savings_account()
    
    
    def accountStatus(self):
        return self.client.account()
    
    
    def assetDetail(self, **kwargs):
        try:
            result = self.client.asset_detail(**kwargs)
            return result
        except Exception:
            pass
    
    
    def tradeFee(self, **kwargs):
        try:
            result = self.client.trade_fee(**kwargs)
            return result
        except Exception:
            pass
     
    
    def orderBook(self, pos_symbol, **kwargs):
        try:
            result = self.client.depth(symbol=pos_symbol, **kwargs)     
            return result
        except Exception:
            pass
           
    
    def bookTicker(self, pos_symbol=''):
        try:
            if pos_symbol != '':
                result = self.client.book_ticker(symbol=pos_symbol)
            else:
                result = self.client.book_ticker()
            return result
        except Exception:
            pass
    
    
    def exchangeInfo(self, pos_symbol='', pos_symbols=[]):
        try:
            if pos_symbol != '':
                result = self.client.exchange_info(symbol=pos_symbol)
            elif not pos_symbols:
                result = self.client.exchange_info()
            else:
                result = self.client.exchange_info(symbols=pos_symbols)
            return result
        except Exception:
            pass
      
                
    def getTickerPrice(self, pos_symbol):
        try:
            result = self.client.ticker_price(symbol=pos_symbol)
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'getTickPrices', 'command_name' : 'get_symbol_ticker', 'result' : result})))
            return -1


    def getAllTickers(self):
        try:
            result = self.client.get_all_tickers()
            return result
        except Exception:
            pass
        

    def getAllSymbols(self):
        try:
            result = self.client.get_all_tickers()
            symbols = [item['symbol'] for item in result]
            return symbols
        except Exception:
            pass
                #self.events_queue.put_nowait(0, ErrorEvent({'function_name' : 'getAllSymbols', 'command_name' : 'get_all_tickers', 'result' : result}))


    def getOrderStatus(self, pos_symbol, pos_orderId, **kwargs):
        try:
            result = self.client.get_order(symbol=pos_symbol, orderId=pos_orderId, **kwargs)
            return result
        except Exception:
            pass


    def getOrders(self, pos_symbol, **kwargs):
        try:
            result = self.client.get_orders(symbol=pos_symbol,  **kwargs)
            return result
        except Exception:
            pass


    def getAllOrders(self, **kwargs):
        try:
            result = []
            symbols_list = self.getAllSymbols()
            for pos_symbol in symbols_list:
                res = self.client.get_orders(symbol=pos_symbol, **kwargs)
                if res:
                    result+=res
            return result
        except:
            pass
        
    
    
    def getOpenOrders(self, pos_symbol=None, **kwargs):
        try:
            result = self.client.get_open_orders(symbol=pos_symbol, **kwargs)
            return result
        except Exception:
            pass
    
    
    def closeOrder(self, pos_symbol, **kwargs):
        try:
            result = self.client.cancel_order(symbol=pos_symbol, **kwargs)
            return result
        except Exception:
            pass


    def openTestPosition(self, pos_symbol, pos_quantity, pos_price):
        try:
            result = self.client.new_order_test(symbol=pos_symbol, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=pos_quantity, price=pos_price)
            return result
        except Exception:
            pass
    
    
    def openPosition(self,pos_symbol,pos_quantity, **kwargs):
        try:
            result = self.client.new_order(symbol = pos_symbol, quantity = pos_quantity, side=SIDE_BUY, type=ORDER_TYPE_MARKET, newOrderRespType='FULL', **kwargs)
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'openPosition', 'command_name' : 'order_market_buy', 'symbol' : pos_symbol,  'quantity' : pos_quantity, 'result' : result})))
   
   
    def closePosition(self,pos_symbol, **kwargs):
        try:
            result = self.client.new_order(symbol=pos_symbol, side=SIDE_SELL, type=ORDER_TYPE_MARKET,  **kwargs)
            
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'closePosition', 'command_name' : 'order_market_sell', 'symbol' : pos_symbol,  'quantity' : pos_quantity, 'result' : result})))
    
    def sellPosition(self,pos_symbol, pos_quantity, pos_price, **kwargs):
        try:
            result = self.client.new_order(symbol=pos_symbol, side=SIDE_SELL, type=ORDER_TYPE_LIMIT, quantity=pos_quantity, price=pos_price, timeInForce=TIME_IN_FORCE_GTC, **kwargs)
            return result
        except Exception:
            pass
    
    def rateLimit(self):
        
        self.client.get_order_rate_limit()
     
    
    
     
    def openStopLossPosition(self,pos_symbol, pos_quantity, pos_stopPrice, **kwargs):
        try:
            result = self.client.new_order(symbol=pos_symbol, side=SIDE_BUY, type=ORDER_TYPE_STOP_LOSS_LIMIT, quantity=pos_quantity, newOrderRespType='FULL', stopPrice = pos_stopPrice, **kwargs)
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'openStopLossPosition', 'command_name' : 'create_order', 'symbol' : pos_symbol, 'price' : pos_price, 'result' : result})))
    
    
    def openTakeProfitPosition(self,pos_symbol, pos_quantity, pos_price, pos_stopPrice, **kwargs):
        try:
            result = self.client.new_order(symbol=pos_symbol, side=SIDE_BUY, type=ORDER_TYPE_TAKE_PROFIT, quantity=pos_quantity, price=pos_price, newOrderRespType='FULL', stopPrice = pos_stopPrice, **kwargs)
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'openStopLossPosition', 'command_name' : 'create_order', 'symbol' : pos_symbol, 'price' : pos_price, 'result' : result})))
    
    
    def openBuyLimitPosition(self, pos_symbol, pos_quantity, pos_price):
        try:
            result = self.client.new_order(symbol=pos_symbol, side=SIDE_BUY, type=ORDER_TYPE_LIMIT, quantity=pos_quantity, price=pos_price, timeInForce=TIME_IN_FORCE_GTC)
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'openBuyLimitPosition', 'command_name' : 'order_buy_limit', 'symbol' : pos_symbol, 'price' : pos_price, 'quantity' : pos_quantity, 'result' : result})))       
    
    
    def openSellLimitPosition(self, pos_symbol, pos_quantity, pos_price):
        try:
            result = self.client.new_order(symbol=pos_symbol, side=SIDE_SELL, type=ORDER_TYPE_LIMIT, quantity=pos_quantity, price=pos_price, timeInForce=TIME_IN_FORCE_GTC)
            return result
        except Exception:
            pass
    
    def modifyBuyLimit(self, pos_symbol, pos_quantity, pos_price, pos_orderId):
        try:
            result = self.client.cancel_order(symbol=pos_symbol, orderId=pos_orderId)
            if(result['status'] == 'CANCELED'):
                result = self.client.new_order(symbol=pos_symbol, side=SIDE_BUY, type=ORDER_TYPE_LIMIT, quantity=pos_quantity, price=pos_price, timeInForce=TIME_IN_FORCE_GTC)
                return result
            else:
                logger.info("Order not canceled")
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'modifyBuyLmit', 'command_name' : 'tradeTransactions', 'orderId' : pos_orderId, 'pos_symbol' : pos_symbol, 'price' : pos_price, 'quantity' : pos_quantity, 'result' : result })))
    
    
    def getRecentTrades(self, pos_symbol, **kwargs):
        try:
            result = self.client.trades(symbol=pos_symbol, **kwargs)
            return result
        except Exception:
            pass
        
        
    def getCoinInfo(self):
        self.client.coin_info(timestamp=datetime.timestamp(datetime.now()))    
                    
    def getMyTrades(self, symbols_list=[]):
        try:
            result = []
            if symbols_list:
                for pos_symbol in symbols_list:
                    result.append(self.client.my_trades(symbol=pos_symbol))
            else:
                res_list = self.getAllSymbols()
                symbols_list = [item['symbol'] for item in res_list]
                for pos_symbol in symbols_list:
                    res = self.client.my_trades(symbol=pos_symbol)
                    if res:
                        result.append(res)
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'getTrades', 'command_name' : 'get_my_trades', 'result' : result})))
            return


    def avgPrice(self, pos_symbol: str = None):
        try:
            result = self.client.avg_price(symbol=pos_symbol)
            return result
        except Exception:
            pass
    
    
    def getTicks24h(self, pos_symbol: str = None):
        try:
            result = self.client.ticker_24hr(symbol=pos_symbol)
            return result
        except Exception:
            pass
      
         
    def getMarginLevel(self):
        try:
            result = self.client.get_asset_balance(asset='money')#?????????????????
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'getMarginLevel', 'command_name' : 'get_asset_balance', 'result' : result})))

   
    def getKlinesFromDate(self, pos_symbol, pos_interval, pos_start):
        try:
            #pos_start = datetime.datetime.strptime(pos_start, '%d-%m-%Y').strftime('%d %b, %Y') 
            #pos_end = date.today().strftime('%d %b, %Y')
            pos_start = int(round(datetime.timestamp(datetime.strptime(pos_start, '%d-%m-%Y'))))
            pos_interval = timeConverter(interval=pos_interval)
            result = self.client.klines(symbol=pos_symbol, interval=pos_interval, startTime=pos_start)
            if result:
                return result
            else:
                result = self.client.klines(symbol=pos_symbol, interval=pos_interval, limit=1000)
                return 1000
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'getData', 'command_name' : 'get_historical_klines', 'symbol' : pos_symbol, 'interval' : pos_interval, 'start_date' : pos_start, 'end_date' : pos_end, 'result' : result})))
    
    
    def getKlinesUntilDate(self, pos_symbol, pos_interval, pos_end):
        try:
            pos_end = int(round(datetime.timestamp(datetime.strptime(pos_end, '%d-%m-%Y'))))
            pos_interval = timeConverter(interval=pos_interval)
            result = self.client.klines(symbol=pos_symbol, interval=pos_interval, endTime=pos_end)
            if result:
                return result
            else:
                result = self.client.klines(symbol=pos_symbol, interval=pos_interval, limit=1000)
                return result
        except Exception:
            pass
       
        
    def getKlinesBetweenDates(self, pos_symbol, pos_interval, pos_start, pos_end, **kwargs):
        try:
            if type(pos_end) == str:
                pos_start = int(round(datetime.timestamp(datetime.strptime(pos_start, '%d-%m-%Y'))))
                pos_end = int(round(datetime.timestamp(datetime.strptime(pos_end, '%d-%m-%Y'))))
            pos_interval = timeConverter(interval=pos_interval)
            result = self.client.klines(symbol=pos_symbol, interval=pos_interval, startTime = pos_start, endTime=pos_end, **kwargs)
            if result:
                return result
            else:
                result = self.client.klines(symbol=pos_symbol, interval=pos_interval, endTime=pos_end, **kwargs)
                if result:
                    return result
                else:
                    result = self.client.klines(symbol=pos_symbol, interval=pos_interval, startTime=pos_start, **kwargs)
                    if result:
                        return result
                    else:
                        result = self.client.klines(symbol=pos_symbol, interval=pos_interval, limit=1000)
                        return result
        except Exception:
            pass
            # self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'getKlinesUntilDate', 'command_name' : 'klines', 'symbol' : pos_symbol, 'interval' : pos_interval, 
            #                                              'end_date' : pos_end, 'result' : result})))
            
    def getLastKlines(self,pos_symbol,pos_interval,pos_limit=500):
        try: 
            result = self.client.klines(symbol=pos_symbol, interval=pos_interval, limit=pos_limit)
            return result
        except Exception:
            pass
                #self.events_queue.put_nowait((0, ErrorEvent({'function_name' : 'getLastTicks', 'command_name' : 'get_historical_klines', 'symbol' : pos_symbol, 'interval' : pos_interval, 'start_date' : pos_start, 'end_date' : pos_end, 'result' : result})))
    
    
    def bookTicker(self, pos_symbol=None):
        try:
            if pos_symbol is None:
                result = self.client.book_ticker()
            else:
                result = self.client.book_ticker(pos_symbol)
            return result
        except Exception:
            pass
    
    def getRecentKline(self, pos_symbol):
        self.client.klines(symbol=pos_symbol, interval='1m', limit=1)
        
    def openStreaming(self):
        result = self.client.new_listen_key()
        return result['listenKey']
    
    def keepAlivestreaming(self, listen_key):
        self.client.renew_listen_key(listen_key)
        
    
    