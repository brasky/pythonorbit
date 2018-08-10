def organizeCoins(tickers, size, BTCcoins, ETHcoins):
    for coin in tickers:
        for minSize in size:
            if coin['trading_pair_id'] == minSize['id']:
                if coin['trading_pair_id'][-3:] == "BTC":
                    if coin['trading_pair_id'] != "ETH-BTC" and coin['trading_pair_id'][-4:] != "USDT":
                        coinData = {
                            "symbol": coin['trading_pair_id'],
                            "askPrice": float(coin['lowest_ask']),
                            "bidPrice": float(coin['highest_bid']),
                            "minVolume": float(minSize['base_min_size'])
                            }
                        BTCcoins.append(coinData)
                if coin['trading_pair_id'][-3:] == "ETH":
                    coinData = {
                        "symbol": coin['trading_pair_id'],
                        "askPrice": float(coin['lowest_ask']),
                        "bidPrice": float(coin['highest_bid']),
                        "minVolume": float(minSize['base_min_size'])
                        }
                    ETHcoins.append(coinData)
                if coin['trading_pair_id'] == "ETH-BTC":
                    ETHBTC = {
                        "symbol": coin['trading_pair_id'],
                        "askPrice": float(coin['lowest_ask']),
                        "bidPrice": float(coin['highest_bid']),
                        "minVolume": float(minSize['base_min_size'])
                        }
                if coin['trading_pair_id'] == "BTC-USDT":
                    USDT = {
                        "symbol": coin['trading_pair_id'],
                        "askPrice": float(coin['lowest_ask']),
                        "bidPrice": float(coin['highest_bid']),
                        "minVolume": float(minSize['base_min_size'])
                    }

    return(BTCcoins, ETHcoins, ETHBTC, USDT)