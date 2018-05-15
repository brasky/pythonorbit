def estimateProfit(beginningBalance, BTCcoins, BNBcoins, ETHcoins, BNBBTC, ETHBTC, minProfit):
    beginningBalance = beginningBalance
    finalResult = []
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
        for bnbcoin in BNBcoins:
            if firstBalance['symbol'] == bnbcoin['symbol'][:-3]:
                symbol = bnbcoin['symbol'][-3:]
                balance = firstBalance['balance'] * bnbcoin['bidPrice']
                maxThru = bnbcoin['bidQty'] * bnbcoin['bidPrice']
                #balance of bnb: NOTE: need to fix maxthru terms, currently they are in bnb or ltc I am not sure...
                secondBalance = {
                    "symbol": symbol,
                    "balance": balance,
                    "maxThru": maxThru
                }

                thirdBalance = {
                    "balance": secondBalance['balance'] * BNBBTC['bidPrice'],
                    "maxThru": BNBBTC['bidQty'] * BNBBTC['bidPrice']
                }
                if thirdBalance['balance'] > minProfit:

                    triangle = {
                        "coin1": firstBalance['symbol'],
                        "coin2": secondBalance['symbol'],
                        "profit": thirdBalance['balance'],
                        "maxThru": min(firstBalance['maxThru'], secondBalance['maxThru'], thirdBalance['maxThru'])
                    }
                    finalResult.append(triangle)
    return finalResult