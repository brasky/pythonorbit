def organizeCoins(tickers, BTCcoins, BNBcoins, ETHcoins):
    for coin in tickers:
        if coin['symbol'][-3:] == "BTC":
            if coin['symbol'] != "BNBBTC" and coin['symbol'] != "ETHBTC" and coin['symbol'][3:] != "USDT":

                coinData = {
                    "symbol": coin['symbol'],
                    "askPrice": float(coin['askPrice']),
                    "askQty": float(coin['askQty']),
                    "bidPrice": float(coin['bidPrice']),
                    "bidQty": float(coin['bidQty'])
                }

                BTCcoins.append(coinData)

        if coin['symbol'][-3:] == "BNB":
            if coin['symbol'][3:] != "USDT":

                coinData = {
                    "symbol": coin['symbol'],
                    "askPrice": float(coin['askPrice']),
                    "askQty": float(coin['askQty']),
                    "bidPrice": float(coin['bidPrice']),
                    "bidQty": float(coin['bidQty'])
                }

                BNBcoins.append(coinData)

        if coin['symbol'][-3:] == "ETH":
            if coin['symbol'] != "BNBETH" and coin['symbol'][3:] != "USDT":
                coinData = {
                    "symbol": coin['symbol'],
                    "askPrice": float(coin['askPrice']),
                    "askQty": float(coin['askQty']),
                    "bidPrice": float(coin['bidPrice']),
                    "bidQty": float(coin['bidQty'])
                }

                ETHcoins.append(coinData)

        if coin['symbol'] == "BNBBTC":
            BNBBTC = {
                "symbol": coin['symbol'],
                "askPrice": float(coin['askPrice']),
                "askQty": float(coin['askQty']),
                "bidPrice": float(coin['bidPrice']),
                "bidQty": float(coin['bidQty'])
            }

        if coin['symbol'] == "ETHBTC":
            ETHBTC = {
                "symbol": coin['symbol'],
                "askPrice": float(coin['askPrice']),
                "askQty": float(coin['askQty']),
                "bidPrice": float(coin['bidPrice']),
                "bidQty": float(coin['bidQty'])
            }

    return(BTCcoins, BNBcoins, ETHcoins, BNBBTC, ETHBTC)
