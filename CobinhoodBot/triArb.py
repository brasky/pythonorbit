import time
import csv
from triangleLogger import *
from cobinhood_api import Cobinhood
cob = Cobinhood(API_TOKEN='***REMOVED***')

def triArb(beginningBal, triangle, ETHBTC):
    print(triangle)
    firstTicker = triangle['coin1']
    secondTicker = triangle['coin2']
    thirdTicker = 'ETH-BTC'
    firstQty = (min(beginningBal, float(triangle['maxThru']))) / float(triangle['coin1Price'])
    #first Qty is in shitcoin terms
    #print(firstQty)
    if firstQty > 500:
        firstQty = int(firstQty)
    #print(firstQty)
    #quit()
    orderOneData = {
        "trading_pair_id": str(firstTicker),
        "side": "bid",
        "type": "market",
        "size": str(firstQty)
    }
    orderOne = cob.trading.post_orders(orderOneData)
    print(logTrade(orderOne))

    # if orderOne:
    #     if orderOne['success'] == 'true':
    #         print("order one successful")
    #         executedQtyOne = float(orderOne['result']['order']['filled'])
    #         #second Qty is also in shitcoin terms
    ordertwoData = {
        "trading_pair_id": str(secondTicker),
        "side": "ask",
        "type": "market",
        "size": str(firstQty)
    }
    orderTwo = cob.trading.post_orders(ordertwoData)
    print(logTrade(orderTwo))

        # else:
        #     print("order one not successful")

    # if orderTwo:
    #     if orderTwo['success'] == 'true':
    #         print("order two successful")
    thirdQty = firstQty * triangle['coin2Price']
    #         #third Qty is in ETH terms
    orderthreeData = {
        "trading_pair_id": 'ETH-BTC',
        "side": "ask",
        "type": "market",
        "size": str(thirdQty)
    }
    orderThree = cob.trading.post_orders(orderthreeData)
    print(logTrade(orderThree))

    #     else:
    #         print("order two not successful")
    #
    # if orderThree['success'] == 'true':
    #     print('order three successful')
    #     executedQtyThree = float(orderThree['result']['order']['filled'])
    # else:
    #     print("order three not successful")

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



# You need to post dict data to api function ex:
#
# # place order
# data = {
#     "trading_pair_id": "BTC-USDT",
#     "side": "bid",
#     "type": "limit",
#     "price": "5000.01000000",
#     "size": "1.0100"
# }
# cobinhood.trade.post_order(data)