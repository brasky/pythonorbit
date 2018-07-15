def organizeCoins(tickers, BTCcoins, ETHcoins):
    for coin in tickers:
        if coin['trading_pair_id'][-3:] == "BTC":
            if coin['trading_pair_id'] != "ETH-BTC" and coin['trading_pair_id'][-4:] != "USDT":
                coinData = {
                    "symbol": coin['trading_pair_id'],
                    "askPrice": float(coin['lowest_ask']),
                    "bidPrice": float(coin['highest_bid'])
                    }
                BTCcoins.append(coinData)
        if coin['trading_pair_id'][-3:] == "ETH":
            coinData = {
                "symbol": coin['trading_pair_id'],
                "askPrice": float(coin['lowest_ask']),
                "bidPrice": float(coin['highest_bid'])
                }
            ETHcoins.append(coinData)
        if coin['trading_pair_id'] == "ETH-BTC":
            ETHBTC = {
                "symbol": coin['trading_pair_id'],
                "askPrice": float(coin['lowest_ask']),
                "bidPrice": float(coin['highest_bid'])}
    return(BTCcoins, ETHcoins, ETHBTC)