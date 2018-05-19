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


influxclient = InfluxDBClient('localhost', parameters.dbport, parameters.dbusername, parameters.dbpassword, parameters.dbname)
influxclient.create_database(parameters.dbname)

client = Client(parameters.apiKey, parameters.apiSecret)
minThru = parameters.minThru
minProfit = parameters.minProfit


def getTickers():
    return client.get_orderbook_tickers()

def getFreeBalance(coin):
    return float(client.get_asset_balance(asset=coin)['free'])

beginningBalance = getFreeBalance('BTC')

def main():
    time.sleep(2)
    firstData = []
    secondData = []
    thirdData = []
    BNBcoins = []
    ETHcoins = []
    BTCcoins = []
    baseCoins = []

    start = time.time()
    tickers = getTickers()

    BTCcoins, BNBcoins, ETHcoins, BNBBTC, ETHBTC = organizeCoins(tickers, BTCcoins, BNBcoins, ETHcoins)
    profitResult, profitPercentLog = estimateProfit(beginningBalance, BTCcoins, BNBcoins, ETHcoins, BNBBTC, ETHBTC, minProfit)
    end = time.time()
    latency = [
        {
            "measurement": "Profit_Estimation_Latency",
            "tags": {
                "Exchange": "Binance"
            },
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "value": end-start
            }
        }
    ]


    # print(end - start)
    for profit in profitPercentLog:
        influxclient.write_points(profit)
    influxclient.write_points(latency)
    print(profitResult)

    if profitResult:
        for triangle in profitResult:
            print("Triangle Found:")
            print("Coins:")
            print("BTC -> " + triangle['coin1'] + " -> " + triangle['coin2'])
            print("Profit %:")
            print(triangle['profit'])
            print("Max Through:")
            print(triangle['maxThru'])


    #if profitResult['profit'] > minProfit:
    #    triArb(profitResult)


while True:
    main()






#
# firstAsk = float(coin['askPrice'])
#
# symbol = coin['symbol']
# qty = float((1 / (firstAsk * 1.001)))
# maxThruOne = float(coin['askQty']) * firstAsk
#
# firstResult = {
#     "symbol": symbol,
#     "qty": qty,
#     "maxThruOne": maxThruOne
# }
#
# firstData.append(firstResult)
################################################################3
#
#
# with open("testing.csv", "w") as result:
#     wr = csv.writer(result, dialect='excel', delimiter=',')
#     while True:
#         start = time.time()
#         for btcShitcoins in tickers:
#         #get first step - BTC to Shitcoin, filter out base pairs
#             if btcShitcoins['symbol'][-3:] == "BTC" and 'BNBBTC' not in btcShitcoins['symbol'] and 'ETHBTC' not in btcShitcoins['symbol'] and 'USDT' not in btcShitcoins['symbol']:
#                 global firstAsk
#                 firstAsk = float(btcShitcoins['askPrice'])
#                 global bid
#                 bid = float(btcShitcoins['bidPrice'])
#                 global firstBalance
#                 firstBalance = {
#                     "symbol": btcShitcoins['symbol'],
#                     "qty": float((1 / (firstAsk*1.001))),
#                     "maxThruOne": float(btcShitcoins['askQty']) * firstAsk
#                 }
#                 firstData.append(firstBalance)
#
#     #get second step - Shitcoin to either BNB or ETH
#         for shitcoins in firstData:
#             for allcoins in tickers:
#                 if shitcoins['symbol'][:-3] == allcoins['symbol'][:-3] and allcoins['symbol'][-3:] != "BTC":
#                     secondBalanceBNB = {
#                         "symbol": allcoins['symbol'],
#                         "qty": firstBalance['qty'] * ((float(allcoins['bidPrice']) / 1.001)),
#                         # price and qty are in BNB terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
#                         "maxThruTwo": (float(allcoins['bidPrice']) * float(allcoins['bidQty'])) * bid
#                     }
#                     secondData.append(secondBalanceBNB)
#
#                 #This never gets used, I'm not sure why this exists. It seems like we are getting all the data we need from the above.
#                 if "ETH" in allcoins and shitcoins['symbol'][:-3] == allcoins['symbol'][:-3]:
#                     global secondBalanceETH
#                     print("DID I MAKE IT HERE?!")
#                     secondBalanceETH = {
#                         "symbol": shitcoins['symbol'],
#                         "qty": firstBalance['qty'] * ((float(shitcoins['bidPrice']) / 1.001)),
#                         # price and qty are in ETH terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
#                         "maxThruTwo": (float(shitcoins['bidPrice']) * float(shitcoins['bidQty'])) * bid
#                     }
#                     secondData.append(secondBalanceETH)
#         # print(firstData)
#         # print(len(secondData))
#         # print(len(firstData))
#         # print(secondData)
#
#         # #get last step - BNB or ETH back to BTC
#         for shitbnbeth in secondData:
#             for allcoinsbtc in tickers:
#                 if 'BTC' in allcoinsbtc['symbol'] and 'USDT' not in allcoinsbtc['symbol']:
#                     if shitbnbeth['symbol'][-3:] == allcoinsbtc['symbol'][:3]:
#                         maxThruThree = float(allcoinsbtc['bidPrice']) * (float(allcoinsbtc['bidQty']))
#                         symbolOne = shitbnbeth['symbol'][:-3] + allcoinsbtc['symbol'][3:]
#                         symbolTwo = shitbnbeth['symbol']
#                         maxThruTwo = float(getSecondBalance(symbolTwo))
#                         maxThruOne = float(getFirstBalance(symbolOne))
#                         thirdBalance = {
#                             "symbol": shitbnbeth['symbol'],
#                             "Ending Balance": float(secondBalanceBNB['qty']) * ((float(allcoinsbtc['bidPrice'])/1.001)),
#                             "maxThruFinal": min(maxThruOne, maxThruTwo, maxThruThree)
#                         }
#
#                         print(thirdBalance)
#
#         break

####################################
#
#
# #get last step - shitcoin back to BTC
#         for bnbcoins in secondData:
#             for allcoins in tickers:
#                 if 'BTC' in allcoins['symbol']:
#                     if bnbcoins['symbol'][:-3] == allcoins['symbol'][:-3]:
#                         # maxThruThree is in bitcoin terms because btc is the base currency
#                         maxThruThree= float(allcoins['bidPrice']) * (float(allcoins['bidQty']))
#                         symbol = bnbcoins['symbol']
#                         #we have to use the getSecondBalance function to ensure that the proper symbol is matched
#                         maxThruTwo = float(getSecondBalance(symbol))
#                         thirdBalance = {
#                             "symbol": allcoins['symbol'],
#                             "Ending Balance": float(bnbcoins['qty']) * ((float(allcoins['bidPrice'])/1.001)),
#                             "maxThruFinal": min(maxThruOne, maxThruTwo, maxThruThree)
#                         }
#                         #uncomment the two below comments to force arb conditions and test the buying function
#                         #thirdBalance['Ending Balance'] = 1.01
#                         #thirdBalance['maxThruFinal'] = 1.111
#                         if thirdBalance['Ending Balance'] > 1.001 and thirdBalance['maxThruFinal'] > 0.001:
#                             secondAsk = float((item for item in tickers if item['symbol'] == bnbcoins['symbol']).__next__()['askPrice'])
#                             thirdBid = float((item for item in tickers if item['symbol'] == thirdBalance['symbol']).__next__()['bidPrice'])
#                             results = triArb("BNBBTC", firstAsk, bnbcoins['symbol'], secondAsk, thirdBalance['symbol'], thirdBid, thirdBalance['maxThruFinal'], thirdBalance['Ending Balance'])
#
#                             print('results: ', results)
#
#                         thirdData.append(thirdBalance)
#                         entry = [bnbcoins['symbol'], float(bnbcoins['qty']) * ((float(allcoins['bidPrice']))/1.001), thirdBalance['maxThruFinal'], time.asctime()]








###############################





#             if 'BNB'in shitcoins['symbol'] and 'BNBBTC' not in shitcoins['symbol'] and 'BNBETH' not in shitcoins['symbol'] and 'BNBUSDT' not in shitcoins['symbol']:
#                 global secondBalanceBNB
#                 secondBalanceBNB = {
#                     "symbol": shitcoins['symbol'],
#                     "qty": firstBalance * ((float(x['bidPrice'])/1.001)),
#                     # price and qty are in BNB terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
#                     "maxThruTwo": (float(shitcoins['bidPrice']) * float(shitcoins['bidQty']))* bid
#                 }
#                 secondData.append(secondBalanceBNB)
#             if 'ETH'in shitcoins['symbol'] and 'BNBETH' not in shitcoins['symbol'] and 'ETHBTC' not in shitcoins['symbol']:
#                 global secondBalanceETH
#                 secondBalanceETH = {
#                     "symbol": shitcoins['symbol'],
#                     "qty": firstBalance * ((float(shitcoins['bidPrice'])/1.001)),
#                     # price and qty are in ETH terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
#                     "maxThruTwo": (float(shitcoins['bidPrice']) * float(shitcoins['bidQty']))* bid
#                 }
#                 secondData.append(secondBalanceETH)
#
# #get last step - BNB or ETH back to BTC
#             #first get price/depth info for both coins
#             if shitcoins['symbol'] == 'ETHBTC':
#                 global ethBid
#                 ethBid = float(shitcoins['bidPrice'])
#                 global ethQty
#                 ethQty = float(shitcoins['bidQty'])
#                 global maxDepthETH
#                 maxDepthETH = ethBid * ethQty
#             if shitcoins['symbol'] == 'BNBBTC':
#                 global bnbBid
#                 bnbBid = float(shitcoins['bidPrice'])
#                 global bnbQty
#                 bnbQty = float(shitcoins['bidQty'])
#                 global maxDepthBNB
#                 maxDepthBNB = bnbBid * bnbQty
#         for coins in secondData:
#             if 'ETH' in coins['symbol']:
#                 symbol = coins['symbol']
#                 maxThruTwo = float(getSecondBalance(symbol))
#                 thirdBalance = {
#                     "symbol": coins['symbol'],
#                     "Ending Balance": float(coins['qty']) * ethBid / 1.001,
#                     "maxThruFinal": min(maxThruOne, maxThruTwo, maxDepthETH)
#                 }
#                 thirdData.append(thirdBalance)
#                 entry = [thirdBalance['symbol'], thirdBalance['Ending Balance'], thirdBalance['maxThruFinal']]
#                 wr.writerow(entry)
#             if 'BNB' in coins['symbol']:
#                 symbol = coins['symbol']
#                 maxThruTwo = float(getSecondBalance(symbol))
#                 thirdBalance = {
#                     "symbol": coins['symbol'],
#                     "Ending Balance": float(coins['qty']) * bnbBid / 1.001,
#                     "maxThruFinal": min(maxThruOne, maxThruTwo, maxDepthBNB)
#                 }
#                 thirdData.append(thirdBalance)
#                 entry = [thirdBalance['symbol'], thirdBalance['Ending Balance'], thirdBalance['maxThruFinal']]
#                 wr.writerow(entry)
#
#         end = time.time()
#         #print(thirdData)
#         print("calculated", len(thirdData), "triangular arbitrage opportunities in", round(end - start, 4), "seconds, at", time.asctime())
#
#
#         time.sleep(2)
#uncomment the two below comments to force arb conditions and test the buying function
                        #thirdBalance['Ending Balance'] = 1.01
                        #thirdBalance['maxThruFinal'] = 1.111
                        #if thirdBalance['Ending Balance'] > 1.001 and thirdBalance['maxThruFinal'] > 0.001:
                            #secondAsk = float((item for item in tickers if item['symbol'] == coins['symbol']).__next__()['askPrice'])
                            #thirdBid = float((item for item in tickers if item['symbol'] == thirdBalance['symbol']).__next__()['bidPrice'])
                            #results = triArb("BNBBTC", firstAsk, coins['symbol'], secondAsk, thirdBalance['symbol'], thirdBid, thirdBalance['maxThruFinal'], thirdBalance['Ending Balance'])

                            #print('results: ', results)