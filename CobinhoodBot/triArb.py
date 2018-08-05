import time
import csv
from organizeCoins import *
from estimateProfit import *
from orbit import *
from cobinhood_api import Cobinhood
cob = Cobinhood(API_TOKEN='***REMOVED***')

def triarb(beginningBal, profitResult, ETHBTC):
    firstTicker = profitResult['coin1']
    secondTicker = profitResult['coin2']
    thirdTicker = 'ETH-BTC'
    firstQty = min(beginningBal, profitResult['maxThru'])

    orderOne = cob.trading.post_orders(
        trading_pair_id = firstTicker,
        side = 'ask',
        type = 'market',
        size = str(firstQty)
    )

    if orderOne['success'] == 'true':
        print("order one successful")
        executedQtyOne = float(orderOne['result']['order']['filled'])

        orderTwo = cob.trading.post_orders(
            trading_pair_id = secondTicker,
            side = 'bid',
            type = 'market',
            size = str(executedQtyOne)
        )
    else:
        print("order one not successful")

    if orderTwo['success'] == 'true':
        print("order two successful")
        executedQtyTwo = float(orderTwo['result']['order']['filled'])
        thirdQty = executedQtyTwo * profitResult['coin2Price']
        orderThree = cob.trading.post_orders(
            trading_pair_id = thirdTicker,
            side = 'bid',
            type = 'market',
            size = str(thirdQty)
        )
    else:
        print("order two not successful")

    if orderThree['success'] == 'true':
        print('order three successful')
        executedQtyThree = float(orderThree['result']['order']['filled'])
    else:
        print("order three not successful")

    balData = cob.wallet.get_balances()
    endingBal = balData['result']['balances'][0]['btc_value']
    return(endingBal)









    #FORMAT OF PROFITRESULT
    # triangle = {
    #     "coin1": shitCoinbalance['symbol'],
    #     "coin1Price": shitCoinbalance['askPrice'],
    #     "coin2": secondBalance['symbol'],
    #     "coin2Price": ethcoin['bidPrice'],
    #     "profit": thirdBalance['balance'],
    #     "maxThru": min(shitCoinbalance['maxThru'], secondBalance['maxThru'], thirdBalance['maxThru'])
    # }