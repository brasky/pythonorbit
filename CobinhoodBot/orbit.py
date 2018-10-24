from setuptools import setup
# setup(name='cobinhood',
#       version='0.1.0',
#       description='Cobinhood API',
#       url='https://github.com/CliffLin/python-cobinhood',
#       author='zylin',
#       packages=['cobinhood_api', 'cobinhood_api.ws', 'cobinhood_api.http'],
#       install_requires=['requests', 'websocket-client', 'coloredlogs'],
#       zip_safe=False)
import time
from triangleLogger import *
import csv
from organizeCoins import *
from estimateProfit import *
from triArb import *
from cobinhood_api import Cobinhood
cob = Cobinhood(API_TOKEN='***REMOVED***')
#print(cob.system.get_time())


def getTickers():
    tickerdata = cob.market.get_tickers()
    return tickerdata['result']['tickers']

def getSize():
    sizedata = cob.market.get_trading_pairs()
    return sizedata['result']['trading_pairs']

def getBal():
    balData = cob.wallet.get_balances()
    return float(balData['result']['balances'][0]['btc_value'])


def main():
    time.sleep(2)
    ETHcoins = []
    BTCcoins = []
    USDT = []

    beginningBal = getBal()
    #print(beginningBal)
    startAPItime = time.time()
    tickers = getTickers()
    size = getSize()
    endAPItime = time.time()
    print('API time: ', endAPItime - startAPItime, 'seconds')
    BTCcoins, ETHcoins, ETHBTC, USDT = organizeCoins(tickers, size, BTCcoins, ETHcoins, USDT)
    triangle = estimateProfit(BTCcoins, ETHcoins, ETHBTC, USDT)
    if triangle:
        print(logTriangle(triangle))
        print("calculated:")
        print(triangle)
        print("triangle found")
        endingBal = float(triArb(beginningBal, triangle, ETHBTC))
        profit = float(endingBal) - float(beginningBal)
        print("profit in BTC terms:", profit)


    # if triangle:
    #     triangle = triangle
    #     print("Triangle Found:")
    #     print("Coins:")
    #     print("BTC -> " + triangle['coin1'] + " -> " + triangle['coin2'])
    #     print("Profit %:")
    #     print(triangle['profit'])

while True:
    main()

