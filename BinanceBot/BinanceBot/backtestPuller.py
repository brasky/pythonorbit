#import api wrapper
import  parameters
import time
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
    triangle = True
    beginningBalance = client.get_asset_balance(asset='BTC')
    print(beginningBalance)
    #this math gets the max possible throughput and truncates down to 2 decimals per binance constraint
    orderoneQty = math.floor(((min((maxAmount / firstAsk), (float(beginningBalance['free']) / firstAsk))))*100)/100
    #note that bnb only allows order quantities that are to 2 decimal points i.e. 1.11 units
    #btc and eth markets allow 3 decimal points i.e. 1.111 units
    orderOne = client.order_market_buy(
        symbol= str(firstSymbol),
        quantity= orderoneQty
        )
    print(orderOne)

    while triangle == True:
        bnbBalance = float(client.get_asset_balance(asset='BNB')['free'])
        #Note that order quantity must be in shitcoin terms. Also the prices are in BNB terms
        #since the first purchase is equal or less to maximum throughput, we can just push the bnb balance through
        ordertwoQty = math.floor(((bnbBalance / secondAsk)) * 100)/100
        if bnbBalance > 0:
            orderTwo = client.order_market_buy(
                symbol= str(secondSymbol),
                quantity= ordertwoQty,
                )
            print(orderTwo)

        if(float(client.get_asset_balance(asset=secondSymbol[:3])['free'])) > 0:
            #prices are in BTC terms, order quantity is in shitcoin terms
            #new fun constraint: binance only allows you to sell integer amounts for shitcoins (btc base currency)
            orderThreeQty = math.floor(float(client.get_asset_balance(asset=thirdSymbol[:3])['free']))
            #at this point we just want to sell all shitcoin to get back to btc
            orderThree = client.order_market_sell(
                symbol= str(thirdSymbol),
                quantity=orderThreeQty,
                )
            print(orderThree)
            triangle = False
    finalBalance = float(client.get_asset_balance(asset='BTC')['free'])
    actualProfit = finalBalance - float(beginningBalance['free'])
    expectedProfit = endingBalance - 1
    arbitrageStats = {
        "Actual Profit": actualProfit,
        "Expected Profit": expectedProfit
    }
    buyEnd = time.time()
    print("Buy time: ", buyEnd - buyStart)
    return arbitrageStats


with open("bnbdata.csv", "w") as result:
    wr = csv.writer(result, dialect='excel', delimiter=',')
    while True:
        global tickers
        tickers = client.get_orderbook_tickers()
        start = time.time()
    #assuming that you have exactly one btc
        global secondData
        secondData = []
        global thirdData
        thirdData = []

        for x in tickers:
        #get first step - BTC to BNB
        #to do: how much bitcoin did you spend
            if 'BNBBTC' in x['symbol']:
                global firstAsk
                firstAsk = float(x['askPrice'])
                global bid
                bid = float(x['bidPrice'])
                global firstBalance
                firstBalance = float((1 / (firstAsk*1.001)))
                global maxThruOne
                #since base currency is BTC, maxThruOne is in btc terms
                maxThruOne = float(x['askQty']) * firstAsk

    #get second step - BNB to shitcoin
    #filter out pairs with the wrong base currency
            if 'BNB'in x['symbol'] and 'BNBBTC' not in x['symbol'] and 'BNBETH' not in x['symbol'] and 'BNBUSDT' not in x['symbol']:
                global secondBalance
                secondBalance = {
                    "symbol": x['symbol'],
                    "qty": firstBalance / ((float(x['askPrice'])*1.001)),
                    # ask price and qty are in BNB terms so "bid" variable brings maxThruTwo to BTC terms. bid will always be lower than ask so it's conservative
                    "maxThruTwo": (float(x['askPrice']) * float(x['askQty']))* bid
                }
                secondData.append(secondBalance)

#get last step - shitcoin back to BTC
        for bnbcoins in secondData:
            for allcoins in tickers:
                if 'BTC' in allcoins['symbol']:
                    if bnbcoins['symbol'][:-3] in allcoins['symbol']:
                        # maxThruThree is in bitcoin terms because btc is the base currency
                        maxThruThree= float(allcoins['bidPrice']) * (float(allcoins['bidQty']))
                        symbol = bnbcoins['symbol']
                        #we have to use the getSecondBalance function to ensure that the proper symbol is matched
                        maxThruTwo = float(getSecondBalance(symbol))
                        thirdBalance = {
                            "symbol": allcoins['symbol'],
                            "Ending Balance": float(bnbcoins['qty']) * ((float(allcoins['bidPrice'])/1.001)),
                            "maxThruFinal": min(maxThruOne, maxThruTwo, maxThruThree)
                        }
                        #uncomment the two below comments to force arb conditions and test the buying function
                        #thirdBalance['Ending Balance'] = 1.01
                        #thirdBalance['maxThruFinal'] = 1.111
                        if thirdBalance['Ending Balance'] > 1 and thirdBalance['maxThruFinal'] > 0.002:
                            secondAsk = float((item for item in tickers if item['symbol'] == bnbcoins['symbol']).__next__()['askPrice'])
                            thirdBid = float((item for item in tickers if item['symbol'] == thirdBalance['symbol']).__next__()['bidPrice'])
                            results = triArb('BNBBTC', firstAsk, bnbcoins['symbol'], secondAsk, thirdBalance['symbol'], thirdBid, thirdBalance['maxThruFinal'], thirdBalance['Ending Balance'])
                            print('results: ', results)
                            quit()

                        thirdData.append(thirdBalance)
                        entry = [bnbcoins['symbol'], float(bnbcoins['qty']) * ((float(allcoins['bidPrice']))/1.001), thirdBalance['maxThruFinal']]
                        wr.writerow(entry)



        end = time.time()
        print(thirdData)
        print(end - start)


        time.sleep(4)
