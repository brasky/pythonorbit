#import api wrapper
import  parameters
import time
import datetime
import csv
import math
import decimal
from binance.client import Client
from binance.enums import *
client = Client(parameters.apiKey, parameters.apiSecret)
    #pull all market data
def getSecondBalance(secondDataSymbol):
        for dict in secondData:
            #print(secondData)
            #print(dict)
            if dict['symbol'] == secondDataSymbol:
                return dict['maxThruTwo']


with open("ethdata.csv", "w") as result:
    wr = csv.writer(result, dialect='excel', delimiter=',')
    while True:
        global beginningBalance
        beginningBalance = float(client.get_asset_balance(asset='BTC')['free'])
        #print("beginning balance is", beginningBalance)
        global tickers
        tickers = client.get_orderbook_tickers()
        wr.writerow(tickers)
        start = time.time()
    #assuming that you have exactly one btc
        global secondData
        secondData = []
        global thirdData
        thirdData = []

        for x in tickers:
        #get first step - BTC to ETH
        #to do: how much bitcoin did you spend
            if 'ETHBTC' in x['symbol']:
                global firstAsk
                firstAsk = float(x['askPrice'])
                global bid
                bid = float(x['bidPrice'])
                global firstBalance
                firstBalance = float((1 / (firstAsk*1.001)))
                global maxThruOne
                #since base currency is BTC, maxThruOne is in btc terms
                maxThruOne = float(x['askQty']) * firstAsk

    #get second step - ETH to shitcoin
    #filter out pairs with the wrong base currency
            if 'ETH'in x['symbol'] and 'ETHBTC' not in x['symbol'] and 'ETHBNB' not in x['symbol'] and 'ETHUSDT' not in x['symbol']:
                global secondBalance
                secondBalance = {
                    "symbol": x['symbol'],
                    "qty": firstBalance / ((float(x['askPrice'])*1.001)),
                    # ask price and qty are in ETH terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
                    "maxThruTwo": (float(x['askPrice']) * float(x['askQty']))* bid
                }
                secondData.append(secondBalance)

#get last step - shitcoin back to BTC
        for ETHcoins in secondData:
            for allcoins in tickers:
                if 'BTC' in allcoins['symbol']:
                    if ETHcoins['symbol'][:-3] == allcoins['symbol'][:-3]:
                        # maxThruThree is in bitcoin terms because btc is the base currency
                        maxThruThree= float(allcoins['bidPrice']) * (float(allcoins['bidQty']))
                        symbol = ETHcoins['symbol']
                        #we have to use the getSecondBalance function to ensure that the proper symbol is matched
                        maxThruTwo = float(getSecondBalance(symbol))
                        thirdBalance = {
                            "symbol": allcoins['symbol'],
                            "Ending Balance": float(ETHcoins['qty']) * ((float(allcoins['bidPrice'])/1.001)),
                            "maxThruFinal": min(maxThruOne, maxThruTwo, maxThruThree)
                        }

                        thirdData.append(thirdBalance)
                        entry = [ETHcoins['symbol'], float(ETHcoins['qty']) * ((float(allcoins['bidPrice']))/1.001), thirdBalance['maxThruFinal'], time.asctime()]
                        wr.writerow(entry)



        end = time.time()
        #print(thirdData)
        print("calculated", len(thirdData), "triangular arbitrage opportunities in", round(end - start, 4), "seconds, at", time.asctime())


        time.sleep(2)
