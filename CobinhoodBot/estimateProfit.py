def estimateProfit(BTCcoins, ETHcoins, ETHBTC, USDT):
    import time
    start = time.time()
    trianglesCalculated = []
    allcalculations = []
    minProfit = 1.01
    #the minimum BTC qty is $25 worth of BTC for our purposes
    #the actual minimum is $20
    #this should be $25 of ETH times the ETHBTC ask price
    for coin in USDT:
        if str(coin['symbol']) == str("ETH-USDT"):
            twentyFiveDollarsofETH = 25 / coin['bidPrice']
            #print(twentyFiveDollarsofETH)
            minBTCqty = twentyFiveDollarsofETH * ETHBTC['askPrice']
    print('minimum order in BTC terms is', minBTCqty)
    #start by calculating triangles in the direction of altcoin -> ETH
    for coin in BTCcoins:
        if coin['askPrice'] != 0 and coin['bidPrice'] != 0:
            symbol = coin['symbol']
            balance = 1.00 / float((coin['askPrice']))
            maxThru = coin['minVolume'] * coin['askPrice']
            # shitCoinbalance is the balance the shitcoin:
            shitCoinbalance = {
                "symbol": symbol,
                "askPrice": coin['askPrice'],
                "bidPrice": coin['bidPrice'],
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
                        "maxThru": (ETHBTC['minVolume'] * ETHBTC['bidPrice'])
                    }
                    allcalculations.append(thirdBalance)
                    if thirdBalance['balance'] > minProfit:
                        triangle = {
                            "coin1": shitCoinbalance['symbol'],
                            "coin1Price": shitCoinbalance['askPrice'],
                            "coin2": secondBalance['symbol'],
                            "coin2Price": ethcoin['bidPrice'],
                            "profit": thirdBalance['balance'],
                            "maxThru": min(shitCoinbalance['maxThru'], secondBalance['maxThru'])
                        }
                        trianglesCalculated.append(triangle)
                        print(triangle)
    #now, calculate all opportunities starting with ETH -> Altcoin
    # for ethcoin in ETHcoins:
    #     symbol = ethcoin['symbol']
    #     maxThruEthcoin = ethcoin['minVolume'] * ethcoin['bidPrice'] / ETHBTC['askPrice']
    #     maxThruETHBTC = (ETHBTC['minVolume'] * ETHBTC['bidPrice'])
    #     #can calculate first and second balance in one line
    #     balance = (float(1 / ETHBTC['askPrice']) / ethcoin['askPrice'])
    #     for coin in BTCcoins:
    #         if coin['symbol'][:-4] == symbol[:-4]:
    #             thirdBalance = balance * coin['bidPrice']
    #             allcalculations.append(thirdBalance)
    #             maxThruCoin = coin['minVolume'] * coin['bidPrice']
    #             maxThru = min(maxThruETHBTC, maxThruEthcoin, maxThruCoin)
    #             if thirdBalance > minProfit:
    #                 triangle = {
    #                     "coin1": ETHBTC['symbol'],
    #                     "coin1Price": ETHBTC['askPrice'],
    #                     "coin2": symbol,
    #                     "coin2Price": ethcoin['askPrice'],
    #                     "profit": thirdBalance,
    #                     "maxThru": maxThru
    #                 }
    #                 trianglesCalculated.append(triangle)
    #                 print(triangle)
    end = time.time()
    calctime = end - start
    print('time to calculate', len(allcalculations), 'opportunities', calctime, 'seconds')
    #now see if there are any executable opportunities - if so, push them to the other module
    highestTriangle = sorted(allcalculations, key=lambda k: k['balance'])[-1]
    print('highest profitability ratio is :', highestTriangle['balance'])
    for triangle in trianglesCalculated:
        if triangle['maxThru'] >= minBTCqty:
            return triangle

