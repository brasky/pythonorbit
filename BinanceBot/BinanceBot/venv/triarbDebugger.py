import math
import decimal
from binance.client import Client
from binance.enums import *
from estimateProfit import *
from organizeCoins import *
from influxdb import InfluxDBClient
from datetime import datetime
from triArb import *
from binance.exceptions import BinanceAPIException
from orbit import *

def Debug(e, triangle, orderOne, orderTwo, orderThree):
    newOrderbook = client.get_orderbook_tickers()
    print("Orderbook changed: Starting Debug")
    #show the parameters that were attempted
    print("attempted parameters:", triangle)
    #show the new orderbook
    for coins newOrderbook:
        if coin['symbol'] == triangle['coin1']:
            actualFirstAsk = float(coin['askPrice'])
        if coin['symbol'] == triangle['coin2']:
            actualSecondBid = float(coin['bidPrice'])
        if coin['symbol'] == "BNBBTC":
            BNBBTC = {
                "symbol": coin['symbol'],
                "askPrice": float(coin['askPrice']),
                "askQty": float(coin['askQty']),
                "bidPrice": float(coin['bidPrice']),
                "bidQty": float(coin['bidQty']),
                "decimals": 2
            }

        if coin['symbol'] == "ETHBTC":
            ETHBTC = {
                "symbol": coin['symbol'],
                "askPrice": float(coin['askPrice']),
                "askQty": float(coin['askQty']),
                "bidPrice": float(coin['bidPrice']),
                "bidQty": float(coin['bidQty']),
                "decimals": 3
            }
            