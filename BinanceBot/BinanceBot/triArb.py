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
    precision = 8
    priceBadFormat = triangle['coin1Price']
    price = '{:0.0{}f}'.format(priceBadFormat, precision)
    firstQtyTheoretical = triangle['maxThru'] / triangle['coin1Price']
    firstQty = (math.floor(firstQtyTheoretical * (10**triangle['coin1Decimals']))/(10**triangle['coin1Decimals']))
    if triangle['coin1Decimals'] == 0:
        firstQty = int(firstQtyTheoretical)
    print("first qty is", firstQty)
    try:

        orderOne = client.order_limit_buy(
            symbol=firstPair,
            quantity=firstQty,
            price=price,
            timeInForce='FOK'
        )
        print(orderOne)
        #market order sells:

        secondPair = triangle['coin2']
        secondQtyTheoretical = float(orderOne['executedQty']) / 1.001
        secondQty = (math.floor(secondQtyTheoretical * (10**triangle['coin2Decimals']))/(10**triangle['coin2Decimals']))
        if triangle['coin2Decimals'] == 0:
            secondQty = int(secondQtyTheoretical)
        print("second qty is", secondQty)
        orderTwo = client.order_market_sell(
            symbol=secondPair,
            quantity=secondQty
        )
        print(orderTwo)
        thirdPair = triangle['coin2'][-3:] + 'BTC'
        #order 2 executed qty is expressed in coin2 terms (not number of BNB or ETH)
        #issue: if the coin2 price changes during execution, you will get a different number of BNB/ETH compared to executed qty
        thirdQtyTheoretical = float(orderTwo['executedQty']) * triangle['coin2Price'] / 1.001

        if thirdPair == "BNBBTC":
            qty = (math.floor(thirdQtyTheoretical * 100)/100)
            print("third qty is", qty)
            print("---------DEBUG STATS:")
            print(thirdPair)
            print("order Two executed: ", orderTwo['executedQty'])
            print("triangle coin 2 price: ", triangle['coin2Price'])
            print("third theoretical: ", thirdQtyTheoretical)
            print("qty :", qty)

            orderThree = client.order_market_sell(
                symbol=thirdPair,
                quantity=qty
            )

        if thirdPair == "ETHBTC":
            qty = (math.floor(thirdQtyTheoretical * 1000) / 1000)
            print("third qty is", qty)
            print("---------DEBUG STATS:")
            print(thirdPair)
            print("order Two executed: ", orderTwo['executedQty'])
            print("triangle coin 2 price: ", triangle['coin2Price'])
            print("third theoretical: ", thirdQtyTheoretical)
            print("qty :", qty)


            orderThree = client.order_market_sell(
                symbol=thirdPair,
                quantity=qty
            )
        print(orderThree)
    except BinanceAPIException as e:
        print("something broke")
        print(e)
        bnbbalanceapi = client.get_asset_balance(asset='BNB')
        ethbalanceapi = client.get_asset_balance(asset='ETH')
        bnbbalance = (math.floor((float(bnbbalanceapi['free'])) * 100)/100)
        ethbalance =(math.floor((float(ethbalanceapi['free'])) * 1000)/1000)
        if bnbbalance > 0.5:
            order = client.order_market_sell(
                symbol='BNBBTC',
                quantity=bnbbalance
            )
        if ethbalance > 0.05:
            order = client.order_market_sell(
                symbol='ETHBTC',
                quantity=ethbalance
            )

    print("done")
