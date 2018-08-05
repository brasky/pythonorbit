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
import csv
from organizeCoins import *
from estimateProfit import *
from cobinhood_api import Cobinhood
cob = Cobinhood(API_TOKEN='***REMOVED***')
#print(cob.system.get_time())


def getTickers():
    return cob.market.get_tickers()

def getSize():
    return cob.market.get_trading_pairs()

def main():
    time.sleep(2)
    ETHcoins = []
    BTCcoins = []

    startAPI = time.time()
    tickerdata = getTickers()
    sizedata = getSize()
    tickers = tickerdata['result']['tickers']
    size = sizedata['result']['trading_pairs']
    endAPI = time.time()
    APItime = endAPI - startAPI
    #print("time to pull market data: ", APItime, "seconds")
    startCalc = time.time()
    BTCcoins, ETHcoins, ETHBTC = organizeCoins(tickers, size, BTCcoins, ETHcoins)
    coinCount = len(ETHcoins) + len(BTCcoins)
    profitResult = estimateProfit(BTCcoins, ETHcoins, ETHBTC)
    endCalc = time.time()
    calcTime = endCalc - startCalc
    #print("time to calculate triangles on",coinCount,"coins:", calcTime, "seconds")




    # if profitResult:
    #     triangle = profitResult
    #     print("Triangle Found:")
    #     print("Coins:")
    #     print("BTC -> " + triangle['coin1'] + " -> " + triangle['coin2'])
    #     print("Profit %:")
    #     print(triangle['profit'])

while True:
    main()

