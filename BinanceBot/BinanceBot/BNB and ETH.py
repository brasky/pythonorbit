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

def triArb(firstSymbol, firstAsk, secondSymbol, secondAsk, thirdSymbol, thirdBid, maxAmount, endingBalance):
    print(firstSymbol, secondSymbol, thirdSymbol, maxAmount)
    buyStart = time.time()
    #this math gets the max possible throughput and truncates down to 2 decimals per binance constraint
    orderoneQty = math.floor((min((maxAmount / firstAsk), beginningBalance / firstAsk))*100)/100
    #note that bnb only allows order quantities that are to 2 decimal points i.e. 1.11 units
    #btc and eth markets allow 3 decimal points i.e. 1.111 units

    orderOne = client.order_market_buy(
        symbol= str(firstSymbol),
        quantity= orderoneQty
        )
    print(orderOne)


    bnbBalance = float(orderOne['executedQty'])
        #bnbBalance = float(client.get_asset_balance(asset='BNB')['free'])
        #Note that order quantity must be in shitcoin terms. Also the prices are in BNB terms
        #since the first purchase is equal or less to maximum throughput, we can just push the bnb balance through
    ordertwoQty = math.floor(((bnbBalance / secondAsk)/1.001) * 100)/100
    print("order two quantity is", ordertwoQty)
    print("second ask is", secondAsk)
    orderTwo = client.order_market_buy(
                symbol= str(secondSymbol),
                quantity= ordertwoQty,
                )
    print(orderTwo)
        #some symbols are not 3 characters long
        #if(float(client.get_asset_balance(asset=secondSymbol[:-3])['free'])) > 0:
            #prices are in BTC terms, order quantity is in shitcoin terms
            #new fun constraint: binance only allows you to sell integer amounts for shitcoins (btc base currency)
    orderThreeQty = math.floor(float(orderTwo['executedQty'])/1.001)
            #at this point we just want to sell all shitcoin to get back to btc
    orderThree = client.order_market_sell(
                symbol= str(thirdSymbol),
                quantity=orderThreeQty,
                )
    print(orderThree)

    finalBalance = float(client.get_asset_balance(asset='BTC')['free'])
    actualProfit = finalBalance - beginningBalance
    expectedProfit = endingBalance - 1
    arbitrageStats = {
        "Actual Profit": actualProfit,
        "Expected Profit": expectedProfit
    }
    buyEnd = time.time()
    print("Buy time: ", buyEnd - buyStart)
    return arbitrageStats


with open("bnbethdata.csv", "w") as result:
    wr = csv.writer(result, dialect='excel', delimiter=',')
    while True:
        global beginningBalance
        beginningBalance = float(client.get_asset_balance(asset='BTC')['free'])
        #print("beginning balance is", beginningBalance)
        global tickers
        tickers = client.get_orderbook_tickers()
        #wr.writerow(tickers)
        start = time.time()
    #assuming that you have exactly one btc
        global secondData
        secondData = []
        global thirdData
        thirdData = []

        for x in tickers:
        #BTC to BNB
            if 'BNBBTC' in x['symbol']:
                global firstAskBNB
                firstAskBNB = float(x['askPrice'])
                global bidBNB
                bidBNB = float(x['bidPrice'])
                global firstBalanceBNB
                firstBalanceBNB = float((1 / (firstAskBNB*1.001)))
                global maxThruOneBNB
                #since base currency is BTC, maxThruOne is in btc terms
                maxThruOneBNB = float(x['askQty']) * firstAskBNB
        #BTC to ETH
            if 'ETHBTC' in x['symbol']:
                global firstAskETH
                firstAskETH = float(x['askPrice'])
                global bidETH
                bidETH = float(x['bidPrice'])
                global firstBalanceETH
                firstBalanceETH = float((1 / (firstAskETH*1.001)))
                global maxThruOneETH
                #since base currency is BTC, maxThruOne is in btc terms
                maxThruOneETH = float(x['askQty']) * firstAskETH

    #get second step - BNB/ETH to shitcoin
    #filter out pairs with the wrong base currency
            if 'BNB'in x['symbol'] and 'BNBBTC' not in x['symbol'] and 'BNBETH' not in x['symbol'] and 'BNBUSDT' not in x['symbol']:
                global secondBalance
                secondBalance = {
                    "symbol": x['symbol'],
                    "qty": firstBalanceBNB / ((float(x['askPrice'])*1.001)),
                    # ask price and qty are in BNB terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
                    "maxThruTwo": (float(x['askPrice']) * float(x['askQty']))* bidBNB
                }
                secondData.append(secondBalance)
            if 'ETH'in x['symbol'] and 'ETHBTC' not in x['symbol'] and 'ETHBNB' not in x['symbol'] and 'ETHUSDT' not in x['symbol']:
                global secondBalance
                secondBalance = {
                    "symbol": x['symbol'],
                    "qty": firstBalanceETH / ((float(x['askPrice'])*1.001)),
                    # ask price and qty are in ETH terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
                    "maxThruTwo": (float(x['askPrice']) * float(x['askQty']))* bidETH
                }
                secondData.append(secondBalance)
#get last step - shitcoin back to BTC
        for arbcoins in secondData:
            for allcoins in tickers:
                if 'BTC' in allcoins['symbol']:
                    if arbcoins['symbol'][:-3] == allcoins['symbol'][:-3]:
                        if arbcoins['symbol'][-3:] =='BNB':
                            global maxThruOne
                            maxThruOne = maxThruOneBNB
                        if arbcoins['symbol'][-3:] =='ETH':
                            global maxThruOne
                            maxThruOne = maxThruOneETH
                        # maxThruThree is in bitcoin terms because btc is the base currency
                        maxThruThree= float(allcoins['bidPrice']) * (float(allcoins['bidQty']))
                        symbol = arbcoins['symbol']
                        #we have to use the getSecondBalance function to ensure that the proper symbol is matched
                        maxThruTwo = float(getSecondBalance(symbol))
                        thirdBalance = {
                            "symbol": arbcoins['symbol'],
                            "Ending Balance": float(arbcoins['qty']) * ((float(allcoins['bidPrice'])/1.001)),
                            "maxThruFinal": min(maxThruOne, maxThruTwo, maxThruThree)
                        }
                        #uncomment the two below comments to force arb conditions and test the buying function
                        #thirdBalance['Ending Balance'] = 1.01
                        #thirdBalance['maxThruFinal'] = 1.111
                        #if thirdBalance['Ending Balance'] > 1 and thirdBalance['maxThruFinal'] > 0.001:
                        #    secondAsk = float((item for item in tickers if item['symbol'] == bnbcoins['symbol']).__next__()['askPrice'])
                        #    thirdBid = float((item for item in tickers if item['symbol'] == thirdBalance['symbol']).__next__()['bidPrice'])
                        #    results = triArb("BNBBTC", firstAsk, bnbcoins['symbol'], secondAsk, thirdBalance['symbol'], thirdBid, thirdBalance['maxThruFinal'], thirdBalance['Ending Balance'])

                        #    print('results: ', results)
                        #    quit()
                        thirdData.append(thirdBalance)
                        entry = thirdBalance['symbol'], thirdBalance['Ending Balance'], thirdBalance['maxThruFinal'], time.asctime()
                        wr.writerow(entry)




        end = time.time()
        #print(thirdData)
        print("calculated", len(thirdData), "triangular arbitrage opportunities in", round(end - start, 4), "seconds, at", time.asctime())


        time.sleep(2)
