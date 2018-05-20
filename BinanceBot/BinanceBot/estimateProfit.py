from influxdb import InfluxDBClient
from datetime import datetime
import parameters
import time

minThru = parameters.minThru


def estimateProfit(beginningBalance, BTCcoins, BNBcoins, ETHcoins, BNBBTC, ETHBTC, minProfit):
    beginningBalance = beginningBalance
    finalResult = []
    profitPercentLog = []
    logTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    testTime = time.time()
    for coin in BTCcoins:
        symbol = coin['symbol']
        balance = 1.00 / (coin['askPrice'] / 1.001)
        maxThru = coin['askQty'] * coin['askPrice'] /1.001
        # firstBalance is the balance the shitcoin:
        firstBalance = {
            "symbol": symbol,
            "askPrice": coin['askPrice'],
            "balance": balance,
            "maxThru": maxThru,
            "decimals": coin['decimals']
        }
        #bnb coins estimate profit
        for bnbcoin in BNBcoins:
            if firstBalance['symbol'][:-3] == bnbcoin['symbol'][:-3]:
                symbol = bnbcoin['symbol']
                balance = firstBalance['balance'] * bnbcoin['bidPrice'] / 1.001
                maxThru = bnbcoin['bidQty'] * bnbcoin['bidPrice'] / BNBBTC['askPrice'] / 1.001
                #balance of bnb: NOTE: by dividing by the BNBBTC ask price, you bring it to BTC terms
                secondBalance = {
                    "symbol": symbol,
                    "balance": balance,
                    "maxThru": maxThru,
                    "decimals": bnbcoin['decimals']
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
                        "coin1Price": firstBalance['askPrice'],
                        "coin1Decimals": firstBalance['decimals'],
                        "coin2": secondBalance['symbol'],
                        "coin2Price": bnbcoin['bidPrice'],
                        "coin2Decimals": secondBalance['decimals'],
                        "profit": thirdBalance['balance'],
                        "maxThru": min(firstBalance['maxThru'], secondBalance['maxThru'], thirdBalance['maxThru'])
                    }
                    if triangle['maxThru'] > minThru:
                        finalResult.append(triangle)
        #eth coins
        for ethcoin in ETHcoins:
            if firstBalance['symbol'][:-3] == ethcoin['symbol'][:-3]:
                symbol = ethcoin['symbol']
                balance = firstBalance['balance'] * ethcoin['bidPrice'] / 1.001
                maxThru = ethcoin['bidQty'] * ethcoin['bidPrice'] / ETHBTC['askPrice'] /1.001
                #balance of eth: NOTE: dividing by the ETHBTC ask price brings it to BTC terms
                secondBalance = {
                    "symbol": symbol,
                    "balance": balance,
                    "maxThru": maxThru,
                    "decimals": ethcoin['decimals']
                }

                thirdBalance = {
                    "balance": secondBalance['balance'] * ETHBTC['bidPrice'] / 1.001,
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
                        "coin1Price": firstBalance['askPrice'],
                        "coin1Decimals": firstBalance['decimals'],
                        "coin2": secondBalance['symbol'],
                        "coin2Price": ethcoin['bidPrice'],
                        "coin2Decimals": secondBalance['decimals'],
                        "profit": thirdBalance['balance'],
                        "maxThru": min(firstBalance['maxThru'], secondBalance['maxThru'], thirdBalance['maxThru'])
                    }
                    if triangle['maxThru'] > minThru:
                        finalResult.append(triangle)

    endTestTime = time.time()
    # print(endTestTime - testTime)
    return finalResult, profitPercentLog