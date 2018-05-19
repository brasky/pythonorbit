#import api wrapper
import  parameters
import time
import datetime
import csv
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


def triArb(client, beginningBalance, triangle, BNBBTC, ETHBTC):
    #first purchase limit order buy

    firstPair = triangle['coin1'] + 'BTC'
    maxThru = triangle['maxThru'] / triangle['coin1Price']
    maxThru = '%.2f'%(maxThru)
    try:

        order = client.order_limit_buy(
            symbol=firstPair,
            quantity=maxThru,
            price=triangle['coin1Price'])

        #market order sells:

        secondPair = triangle['coin1'] + triangle['coin2']
        order = client.order_market_sell(
            symbol=secondPair,
            quantity=maxThru)

        thirdPair = triangle['coin2'] + 'BTC'
        if thirdPair == "BNBBTC":
            qty = '%.2f'%(float(maxThru) * triangle['coin2Price'])
            order = client.order_market_sell(
                symbol=thirdPair,
                quantity=qty)

        if thirdPair == "ETHBTC":
            qty = '%.2f'%(float(maxThru) * triangle['coin2Price'])
            order = client.order_market_sell(
                symbol=thirdPair,
                quantity=qty)

    except BinanceAPIException as e:
        print("something broke")
        print(e)

    print("done")
