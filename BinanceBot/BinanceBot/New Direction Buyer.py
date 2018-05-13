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

#def triArb(firstSymbol, firstAsk, secondSymbol, secondAsk, thirdSymbol, thirdBid, maxAmount, endingBalance):
    #print(firstSymbol, secondSymbol, thirdSymbol, maxAmount)
    #buyStart = time.time()
    #this math gets the max possible throughput and truncates down to 2 decimals per binance constraint
    #orderoneQty = math.floor((min((maxAmount / firstAsk), beginningBalance / firstAsk))*100)/100
    #note that bnb only allows order quantities that are to 2 decimal points i.e. 1.11 units
    #btc and eth markets allow 3 decimal points i.e. 1.111 units

    #orderOne = client.order_market_buy(
    #    symbol= str(firstSymbol),
    #    quantity= orderoneQty
     #   )
    #print(orderOne)

    #
    # bnbBalance = float(orderOne['executedQty'])
    #     #bnbBalance = float(client.get_asset_balance(asset='BNB')['free'])
    #     #Note that order quantity must be in shitcoin terms. Also the prices are in BNB terms
    #     #since the first purchase is equal or less to maximum throughput, we can just push the bnb balance through
    # ordertwoQty = math.floor(((bnbBalance / secondAsk)/1.001) * 100)/100
    # print("order two quantity is", ordertwoQty)
    # print("second ask is", secondAsk)
    # #orderTwo = client.order_market_buy(
    # #             symbol= str(secondSymbol),
    # #             quantity= ordertwoQty,
    # #             )
    # # print(orderTwo)
    # #     #some symbols are not 3 characters long
    # #     #if(float(client.get_asset_balance(asset=secondSymbol[:-3])['free'])) > 0:
    # #         #prices are in BTC terms, order quantity is in shitcoin terms
    # #         #new fun constraint: binance only allows you to sell integer amounts for shitcoins (btc base currency)
    # orderThreeQty = math.floor(float(orderTwo['executedQty'])/1.001)
    #         #at this point we just want to sell all shitcoin to get back to btc
    # #orderThree = client.order_market_sell(
    #             symbol= str(thirdSymbol),
    #             quantity=orderThreeQty,
    #             )
    # print(orderThree)
    #
    # finalBalance = float(client.get_asset_balance(asset='BTC')['free'])
    # actualProfit = finalBalance - beginningBalance
    # expectedProfit = endingBalance - 1
    # arbitrageStats = {
    #     "Actual Profit": actualProfit,
    #     "Expected Profit": expectedProfit
    # }
    # buyEnd = time.time()
    # print("Buy time: ", buyEnd - buyStart)
    # return arbitrageStats
    #

with open("testing.csv", "w") as result:
    wr = csv.writer(result, dialect='excel', delimiter=',')
    while True:
        global beginningBalance
        beginningBalance = float(client.get_asset_balance(asset='BTC')['free'])
        global tickers
        tickers = client.get_orderbook_tickers()
        start = time.time()
        global firstData
        firstData = []
        global secondData
        secondData = []
        global thirdData
        thirdData = []

        for shitcoins in tickers:
        #get first step - BTC to Shitcoin, filter out base pairs
            if shitcoins['symbol'][-3:] == "BTC" and 'BNBBTC' not in shitcoins['symbol'] and 'ETHBTC' not in shitcoins['symbol'] and 'USDT' not in shitcoins['symbol']:
                global firstAsk
                firstAsk = float(shitcoins['askPrice'])
                global bid
                bid = float(shitcoins['bidPrice'])
                global firstBalance
                firstBalance = {
                    "symbol": shitcoins['symbol'],
                    "qty": float((1 / (firstAsk*1.001))),
                    "maxThruOne": float(shitcoins['askQty']) * firstAsk
                }
                firstData.append(firstBalance)

    #get second step - Shitcoin to either BNB or ETH
        for shitcoins in firstData:
            print(shitcoins['symbol'][:-3])
            for allcoins in tickers:
                if shitcoins['symbol'][:-3] == allcoins['symbol'][:-3]:
                    print(allcoins)
                    secondBalanceBNB = {
                        "symbol": allcoins['symbol'],
                        "qty": firstBalance['qty'] * ((float(allcoins['bidPrice']) / 1.001)),
                        # price and qty are in BNB terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
                        "maxThruTwo": (float(shitcoins['bidPrice']) * float(shitcoins['bidQty'])) * bid
                    }
                    print(secondBalanceBNB)
                    secondData.append(secondBalanceBNB)

                if "ETH" in allcoins and shitcoins['symbol'][:-3] == allcoins['symbol'][:-3]:
                    global secondBalanceETH
                    secondBalanceETH = {
                        "symbol": shitcoins['symbol'],
                        "qty": firstBalance['symbol'] * ((float(shitcoins['bidPrice']) / 1.001)),
                        # price and qty are in ETH terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
                        "maxThruTwo": (float(shitcoins['bidPrice']) * float(shitcoins['bidQty'])) * bid
                    }
                    secondData.append(secondBalanceETH)
        print(firstData)
        print(secondData)
        break









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