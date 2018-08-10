def estimateProfit(BTCcoins, ETHcoins, ETHBTC, USDT):
    with open("testing.csv", "w") as result:
        import csv
        wr = csv.writer(result, dialect='excel', delimiter=',')
        finalResult = []
        profitPercentLog = []
        #logTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        minProfit = 1
        #testTime = time.time()
        #the minimum BTC qty is $25 worth of BTC for our purposes
        minBTCqty = 25 / USDT['bidPrice']
        print(minBTCqty)
        for coin in BTCcoins:
            symbol = coin['symbol']
            balance = 1.00 / (coin['askPrice'])
            maxThru = coin['minVolume'] * coin['askPrice']
            # shitCoinbalance is the balance the shitcoin:
            shitCoinbalance = {
                "symbol": symbol,
                "askPrice": coin['askPrice'],
                "balance": balance,
                "maxThru": maxThru,
                #"decimals": coin['decimals']
            }
            #print(shitCoinbalance['symbol'][:-4])
            #eth coins
            for ethcoin in ETHcoins:
                #print(ethcoin)
                if shitCoinbalance['symbol'][:-4] == ethcoin['symbol'][:-4]:
                    symbol = ethcoin['symbol']
                    balance = shitCoinbalance['balance'] * ethcoin['bidPrice']
                    #maxThru = ethcoin['minVolume'] * ethcoin['bidPrice']
                    maxThru = ethcoin['minVolume'] * ethcoin['bidPrice'] / ETHBTC['askPrice']
                    #balance of eth: NOTE: dividing by the ETHBTC ask price brings it to BTC terms
                    secondBalance = {
                        "symbol": symbol,
                        "balance": balance,
                        "maxThru": maxThru,
                        #"decimals": ethcoin['decimals']
                    }
                    #print(secondBalance)
                    thirdBalance = {
                        "balance": secondBalance['balance'] * ETHBTC['bidPrice'],
                        "maxThru": (ETHBTC['minVolume'] * ETHBTC['bidPrice'])*1.5
                    }
                    if thirdBalance['balance'] > minProfit:
#manually overwriting the ETH minimum throughput for volatility concerns.
                        triangle = {
                            "coin1": shitCoinbalance['symbol'],
                            "coin1Price": shitCoinbalance['askPrice'],
                            "coin2": secondBalance['symbol'],
                            "coin2Price": ethcoin['bidPrice'],
                            "profit": thirdBalance['balance'],
                            "maxThru": min(shitCoinbalance['maxThru'], secondBalance['maxThru'])
                        }
                        # finalResult.append(triangle)
                        # #print(triangle)
                        # entry = triangle
                        # wr.writerow(entry)
                        if triangle['maxThru'] >= minBTCqty:
        #endTestTime = time.time()
        # print(endTestTime - testTime)
                            return triangle