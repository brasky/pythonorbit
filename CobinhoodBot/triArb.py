import time
import csv
from cobinhood_api import Cobinhood
cob = Cobinhood(API_TOKEN='***REMOVED***')

def triArb(beginningBal, profitResult, ETHBTC):
    print(profitResult)
    firstTicker = profitResult['coin1']
    secondTicker = profitResult['coin2']
    thirdTicker = 'ETH-BTC'
    firstQty = (min(beginningBal, float(profitResult['maxThru'])))/float(profitResult['coin1Price'])
    #first Qty is in shitcoin terms
    #print(firstQty)
    if firstQty > 500:
        firstQty = int(firstQty)
    #print(firstQty)
    #quit()
    orderOne = cob.trading.post_orders(
        trading_pair_id = firstTicker,
        #side = 'ask',
        type = 'market',
        size = str(firstQty)
    )

    if orderOne['success'] == 'true':
        print("order one successful")
        executedQtyOne = float(orderOne['result']['order']['filled'])
        #second Qty is also in shitcoin terms
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
        #third Qty is in ETH terms
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