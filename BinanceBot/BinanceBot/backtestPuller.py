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

def triArb(firstSymbol, firstAsk, secondSymbol, secondAsk, thirdSymbol, thirdBid, maxAmount):
    print(firstSymbol, secondSymbol, thirdSymbol, maxAmount)
    orderOne = client.create_test_order(
        symbol= firstSymbol,
        side=SIDE_BUY,
        type='MARKET',
        timeInForce='FOK',
        quantity= maxAmount,
        price= firstAsk)
    orderTwo = client.create_test_order(
        symbol= secondSymbol,
        side=SIDE_BUY,
        type='MARKET',
        timeInForce='FOK',
        quantity=maxAmount,
        price=secondAsk)
    orderThree = client.create_test_order(
        symbol= thirdSymbol,
        side=SIDE_SELL,
        type='MARKET',
        timeInForce='FOK',
        quantity=maxAmount,
        price=thirdBid)
    print(orderOne)
    print(orderTwo)
    print(orderThree)

with open("bnbdata.csv", "w") as result:
    wr = csv.writer(result, dialect='excel', delimiter=',')
    while True:
        global tickers
        tickers = client.get_orderbook_tickers()
        start = time.time()
    #print(tickers)
    #assuming that you have exactly one btc
        global secondData
        secondData = []
        global thirdData
        thirdData = []
#get first two steps in one for loop
        for x in tickers:
        #get first step - BNBBTC ask price
        #to do: how much bitcoin did you spend
            if 'BNBBTC' in x['symbol']:
                firstAsk = float(x['askPrice'])
                global bid
                bid = float(x['bidPrice'])
                global firstBalance
                firstBalance = float((1 / (firstAsk*1.001)))
                global maxThruOne
                maxThruOne = float(x['askQty']) * firstAsk
            #print(firstBalance, "BNB")
    #get second step - quantity of shitcoin that you got for selling that BNB you just bought
    #filter out pairs with the wrong base currency
            if 'BNB'in x['symbol'] and 'BNBBTC' not in x['symbol'] and 'BNBETH' not in x['symbol'] and 'BNBUSDT' not in x['symbol']:
                global secondBalance
                secondBalance = {
                    "symbol": x['symbol'],
                    "qty": firstBalance / ((float(x['askPrice'])*1.001)),
                    "maxThruTwo": (float(x['askPrice']) * float(x['askQty']))* bid
                }
                #print(x['symbol'])
                #print("ask price is", x['askPrice'])
                #print("askQty is ", x['askQty'])
                #print("two", secondBalance['maxThruTwo'])
                #print("max thru one is", maxThruOne)
                secondData.append(secondBalance)

#get last step
        for x in secondData:
            for y in tickers:
                if 'BTC' in y['symbol']:
                    if x['symbol'][:-3] in y['symbol']:
                        maxThruThree= float(y['bidPrice']) * (float(y['bidQty']))
                        symbol = x['symbol']
                        #print(getSecondBalance(symbol))
                        maxThruTwo = float(getSecondBalance(symbol))
                        #print(secondData)
                        thirdBalance = {
                            "symbol": x['symbol'],
                            "Ending Balance": float(x['qty']) * ((float(y['bidPrice'])/1.001)),
                            "maxThruFinal": min(maxThruOne, maxThruTwo, maxThruThree)
                        }
                        if thirdBalance['Ending Balance'] > 1 and thirdBalance['maxThruFinal'] > 0.005:
                            secondAsk = float((item for item in tickers if item['symbol'] == secondBalance['symbol']).next()['askPrice'])
                            thirdBid = float((item for item in tickers if item['symbol'] == thirdBalance['symbol']).next()['bidPrice'])
                            triArb('BNBBTC', firstAsk, secondBalance['symbol'], secondAsk, thirdBalance['symbol'], thirdBid, thirdBalance['maxThruFinal'])
                            quit()
                        #print(x['symbol'])
                        #print("bid price is", y['bidPrice'])
                        #print("bidQty is ", y['bidQty'])
                        #print("third", maxThruThree)
                        #print("max thru one is", maxThruOne)

                        thirdData.append(thirdBalance)
                        entry = [x['symbol'], float(x['qty']) * ((float(y['bidPrice']))/1.001), maxThruThree]
                        wr.writerow(entry)



        end = time.time()
        print(thirdData)
        #print(end - start)
        #print(tickers)

        time.sleep(2)
