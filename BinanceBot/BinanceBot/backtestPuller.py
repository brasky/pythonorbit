#import api wrapper
import  parameters
import time
import csv
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
    orderOne = client.create_test_order(
        symbol= firstSymbol,
        side='BUY',
        type='MARKET',
        timeInForce='FOK',
        quantity= maxAmount,
        price= firstAsk)
    print(orderOne)

    while(triangle == True):
        if(client.get_asset_balance(asset=firstSymbol[:3] > 0)):
            secondAmount = client.get_asset_balance(asset=firstSymbol[:3])
            orderTwo = client.create_test_order(
                symbol= secondSymbol,
                side='BUY',
                type='MARKET',
                timeInForce='FOK',
                quantity=secondAmount,
                price=secondAsk)
            print(orderTwo)
        if(client.get_asset_balance(asset=secondSymbol[:3]) > 0):
            thirdAmount = client.get_asset_balance(asset=firstSymbol[:3])
            orderThree = client.create_test_order(
                symbol= thirdSymbol,
                side='SELL',
                type='MARKET',
                timeInForce='FOK',
                quantity=thirdAmount,
                price=thirdBid)
            print(orderThree)
            triangle = False
    finalBalance = float(client.get_asset_balance(asset='BTC'))
    actualProfit = beginningBalance - finalBalance
    expectedProfit = endingBalance - 1
    arbitrageStats = {
        "Actual Profit": actualProfit,
        "Expected Profit": expectedProfit
    }
    buyEnd = time.time()
    print("Buy time: ", buyStart - buyEnd)
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

                        if thirdBalance['Ending Balance'] > 1 and thirdBalance['maxThruFinal'] > 0.002:
                            secondAsk = float((item for item in tickers if item['symbol'] == bnbcoins['symbol']).next()['askPrice'])
                            thirdBid = float((item for item in tickers if item['symbol'] == thirdBalance['symbol']).next()['bidPrice'])
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
