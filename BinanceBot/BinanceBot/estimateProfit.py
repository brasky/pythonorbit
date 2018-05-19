from influxdb import InfluxDBClient
from datetime import datetime
import parameters
import time

def estimateProfit(beginningBalance, BTCcoins, BNBcoins, ETHcoins, BNBBTC, ETHBTC, minProfit):
    beginningBalance = beginningBalance
    finalResult = []
    profitPercentLog = []
    logTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    testTime = time.time()
    for coin in BTCcoins:
        symbol = coin['symbol'][:-3]
        balance = 1.00 / coin['askPrice'] / 1.001
        maxThru = coin['askQty'] * coin['askPrice']
        # firstBalance is the balance the shitcoin:
        firstBalance = {
            "symbol": symbol,
            "balance": balance,
            "maxThru": maxThru
        }
        #bnb coins estimate profit
        for bnbcoin in BNBcoins:
            if firstBalance['symbol'] == bnbcoin['symbol'][:-3]:
                symbol = bnbcoin['symbol'][-3:]
                balance = firstBalance['balance'] * bnbcoin['bidPrice'] / 1.001
                maxThru = bnbcoin['bidQty'] * bnbcoin['bidPrice']
                #balance of bnb: NOTE: need to fix maxthru terms, currently they are in bnb or shit I am not sure...
                secondBalance = {
                    "symbol": symbol,
                    "balance": balance,
                    "maxThru": maxThru
                }

                thirdBalance = {
                    "balance": secondBalance['balance'] * BNBBTC['bidPrice'] / 1.001,
                    "maxThru": BNBBTC['bidQty'] * BNBBTC['bidPrice']
                }
                possibeTriangle = {
                    "coin1": "BTC",
                    "coin2": firstBalance['symbol'],
                    "coin3": secondBalance['symbol']
                }
                profitPercent = [
                    {
                        "measurement": "Profit_Percentage",
                        "tags": {
                            "Exchange": "Binance",
                            "triangle": "" + possibeTriangle["coin1"] + "-" + possibeTriangle["coin2"] + "-" +
                                        possibeTriangle["coin3"]

                        },
                        "time": logTime,
                        "fields": {
                            "profit": thirdBalance['balance'],
                            "triangle": "" + possibeTriangle["coin1"] + "-" + possibeTriangle["coin2"] + "-" +
                                        possibeTriangle["coin3"]

                        }
                    }
                ]
                profitPercentLog.append(profitPercent)
                if thirdBalance['balance'] > minProfit:

                    triangle = {
                        "coin1": firstBalance['symbol'],
                        "coin2": secondBalance['symbol'],
                        "profit": thirdBalance['balance'],
                        "maxThru": min(firstBalance['maxThru'], secondBalance['maxThru'], thirdBalance['maxThru'])
                    }
                    finalResult.append(triangle)
        #eth coins
        for ethcoin in ETHcoins:
            if firstBalance['symbol'] == ethcoin['symbol'][:-3]:
                symbol = ethcoin['symbol'][-3:]
                balance = firstBalance['balance'] * ethcoin['bidPrice']
                maxThru = ethcoin['bidQty'] * ethcoin['bidPrice']
                #balance of eth: NOTE: need to fix maxthru terms, currently they are in eth or shit I am not sure...
                secondBalance = {
                    "symbol": symbol,
                    "balance": balance,
                    "maxThru": maxThru
                }

                thirdBalance = {
                    "balance": secondBalance['balance'] * ETHBTC['bidPrice'],
                    "maxThru": ETHBTC['bidQty'] * ETHBTC['bidPrice']
                }
                possibeTriangle = {
                    "coin1": "BTC",
                    "coin2": firstBalance['symbol'],
                    "coin3": secondBalance['symbol']
                }
                profitPercent = [
                    {
                        "measurement": "Profit_Percentage",
                        "tags": {
                            "Exchange": "Binance",
                            "triangle": "" + possibeTriangle["coin1"] + "-" + possibeTriangle["coin2"] + "-" +
                                        possibeTriangle["coin3"]

                        },
                        "time": logTime,
                        "fields": {
                            "profit": thirdBalance['balance'],
                            "triangle": "" + possibeTriangle["coin1"] + "-" + possibeTriangle["coin2"] + "-" +
                                        possibeTriangle["coin3"]

                        }
                    }
                ]
                profitPercentLog.append(profitPercent)
                if thirdBalance['balance'] > minProfit:

                    triangle = {
                        "coin1": firstBalance['symbol'],
                        "coin2": secondBalance['symbol'],
                        "profit": thirdBalance['balance'],
                        "maxThru": min(firstBalance['maxThru'], secondBalance['maxThru'], thirdBalance['maxThru'])
                    }
                    finalResult.append(triangle)

    endTestTime = time.time()
    # print(endTestTime - testTime)
    return finalResult, profitPercentLog