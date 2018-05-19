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

    firstPair = triangle['coin1']
    firstQtyTheoretical = triangle['maxThru'] / triangle['coin1Price']
    firstQty = (math.floor(firstQtyTheoretical * (10**triangle['coin1Decimals']))/(10**triangle['coin1Decimals']))
    try:

        orderOne = client.order_limit_buy(
            symbol=firstPair,
            quantity=firstQty,
            price=triangle['coin1Price']
        )

        #market order sells:

        secondPair = triangle['coin2']
        secondQtyTheoretical = orderOne['executedQty'] / 1.001
        secondQty = (math.floor(secondQtyTheoretical * (10**triangle['coin2Decimals']))/(10**triangle['coin2Decimals']))
        orderTwo = client.order_market_sell(
            symbol=secondPair,
            quantity=secondQty
        )

        thirdPair = triangle['coin2'][-3:] + 'BTC'
        thirdQtyTheoretical = orderTwo['executedQty'] / 1.001
        if thirdPair == "BNBBTC":
            qty = (math.floor(thirdQtyTheoretical * 100)/100)
            orderThree = client.order_market_sell(
                symbol=thirdPair,
                quantity=qty
            )

        if thirdPair == "ETHBTC":
            qty = (math.floor(thirdQtyTheoretical * 1000) / 1000)
            orderThree = client.order_market_sell(
                symbol=thirdPair,
                quantity=qty
            )

    except BinanceAPIException as e:
        print("something broke")
        print(e)

    print("done")
