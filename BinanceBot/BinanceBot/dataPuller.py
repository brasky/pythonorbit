import parameters
import csv
import time
from binance.client import Client
client = Client(parameters.apiKey, parameters.apiSecret)
# get prices
with open("data.csv", 'w') as result:
    wr = csv.writer(result, dialect= 'excel', delimiter = ',')
    while True:
    # pull the bid/ask for the first pair
        depthOne = str(client.get_orderbook_ticker(symbol="BNBBTC"))
        bidLocOne = depthOne.index('bidPrice')
        askLocOne = depthOne.index('askPrice')
        bidPriceOne = float(depthOne[bidLocOne + 12:bidLocOne + 22])
        askPriceOne = float(depthOne[askLocOne + 12:askLocOne + 22])

    # pull the bid/ask for the second pair
        depthTwo = str(client.get_orderbook_ticker(symbol="XZCBNB"))
        bidLocTwo = depthTwo.index('bidPrice')
        askLocTwo = depthTwo.index('askPrice')
        bidPriceTwo = float(depthTwo[bidLocTwo + 12:bidLocTwo + 22])
        askPriceTwo = float(depthTwo[askLocTwo + 12:askLocTwo + 22])

    # pull the bid/ask for the final pair
        depthThree = str(client.get_orderbook_ticker(symbol="XZCBTC"))
        bidLocThree = depthThree.index('bidPrice')
        askLocThree = depthThree.index('askPrice')
        bidPriceThree = float(depthThree[bidLocThree + 12:bidLocThree + 22])
        askPriceThree = float(depthThree[askLocThree + 12:askLocThree + 22])

    # do the math to determine if there is a triangular arbitrage opportunity
        arbIndex = 1 / (askPriceOne * 1.001) / (askPriceTwo * 1.001) * (bidPriceThree * 0.999)
        print("arbitrage index is", arbIndex)
        entry = ["XZC", time, arbIndex]
        wr.writerow(entry)
        time.sleep(10)
