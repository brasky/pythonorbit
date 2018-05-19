def organizeCoins(tickers, BTCcoins, BNBcoins, ETHcoins):
    for coin in tickers:
        if coin['symbol'][-3:] == "BTC":
            if coin['symbol'] != "BNBBTC" and coin['symbol'] != "ETHBTC" and coin['symbol'][3:] != "USDT":
                decimals = (coin['askQty'].rstrip("0"))[::-1].find('.')
                coinData = {
                    "symbol": coin['symbol'],
                    "askPrice": float(coin['askPrice']),
                    "askQty": float(coin['askQty']),
                    "bidPrice": float(coin['bidPrice']),
                    "bidQty": float(coin['bidQty']),
                    "decimals": int(decimals)
                }

                BTCcoins.append(coinData)

        if coin['symbol'][-3:] == "BNB":
            if coin['symbol'][3:] != "USDT":
                decimals = (coin['bidQty'].rstrip("0"))[::-1].find('.')
                coinData = {
                    "symbol": coin['symbol'],
                    "askPrice": float(coin['askPrice']),
                    "askQty": float(coin['askQty']),
                    "bidPrice": float(coin['bidPrice']),
                    "bidQty": float(coin['bidQty']),
                    "decimals": int(decimals)
                }

                BNBcoins.append(coinData)

        if coin['symbol'][-3:] == "ETH":
            if coin['symbol'] != "BNBETH" and coin['symbol'][3:] != "USDT":
                decimals = (coin['bidQty'].rstrip("0"))[::-1].find('.')
                coinData = {
                    "symbol": coin['symbol'],
                    "askPrice": float(coin['askPrice']),
                    "askQty": float(coin['askQty']),
                    "bidPrice": float(coin['bidPrice']),
                    "bidQty": float(coin['bidQty']),
                    "decimals": int(decimals)
                }

                ETHcoins.append(coinData)

        if coin['symbol'] == "BNBBTC":
            BNBBTC = {
                "symbol": coin['symbol'],
                "askPrice": float(coin['askPrice']),
                "askQty": float(coin['askQty']),
                "bidPrice": float(coin['bidPrice']),
                "bidQty": float(coin['bidQty']),
                "decimals": 2
            }

        if coin['symbol'] == "ETHBTC":
            ETHBTC = {
                "symbol": coin['symbol'],
                "askPrice": float(coin['askPrice']),
                "askQty": float(coin['askQty']),
                "bidPrice": float(coin['bidPrice']),
                "bidQty": float(coin['bidQty']),
                "decimals": 3
            }
    return(BTCcoins, BNBcoins, ETHcoins, BNBBTC, ETHBTC)
