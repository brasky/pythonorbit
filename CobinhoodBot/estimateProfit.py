def estimateProfit(BTCcoins, ETHcoins, ETHBTC):
    with open("testing.csv", "w") as result:
        import csv
        wr = csv.writer(result, dialect='excel', delimiter=',')
        finalResult = []
        profitPercentLog = []
        #logTime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        minProfit = 1
        #testTime = time.time()
        for coin in BTCcoins:
            symbol = coin['symbol']
            balance = 1.00 / (coin['askPrice'])
            #maxThru = coin['askQty'] * coin['askPrice']
            # firstBalance is the balance the shitcoin:
            firstBalance = {
                "symbol": symbol,
                "askPrice": coin['askPrice'],
                "balance": balance,
                #"maxThru": maxThru,
                #"decimals": coin['decimals']
            }
            #print(firstBalance['symbol'][:-4])
            #eth coins
            for ethcoin in ETHcoins:
                #print(ethcoin)
                if firstBalance['symbol'][:-4] == ethcoin['symbol'][:-4]:
                    symbol = ethcoin['symbol']
                    balance = firstBalance['balance'] * ethcoin['bidPrice']
                    #maxThru = ethcoin['bidQty'] * ethcoin['bidPrice'] / ETHBTC['askPrice']
                    #balance of eth: NOTE: dividing by the ETHBTC ask price brings it to BTC terms
                    secondBalance = {
                        "symbol": symbol,
                        "balance": balance,
                        #"maxThru": maxThru,
                        #"decimals": ethcoin['decimals']
                    }
                    #print(secondBalance)
                    thirdBalance = {
                        "balance": secondBalance['balance'] * ETHBTC['bidPrice'],
                        #"maxThru": ETHBTC['bidQty'] * ETHBTC['bidPrice']
                    }
                    if thirdBalance['balance'] > minProfit:

                        triangle = {
                            "coin1": firstBalance['symbol'],
                            "coin1Price": firstBalance['askPrice'],
                            "coin2": secondBalance['symbol'],
                            "coin2Price": ethcoin['bidPrice'],
                            "profit": thirdBalance['balance']
                            #"maxThru": min(firstBalance['maxThru'], secondBalance['maxThru'], thirdBalance['maxThru'])
                        }
                        finalResult.append(triangle)
                        entry = triangle
                        wr.writerow(entry)
        #endTestTime = time.time()
        # print(endTestTime - testTime)
        return finalResult