import  parameters
import math
import time
from binance.client import Client
client = Client(parameters.apiKey, parameters.apiSecret)
orderOne = client.create_test_order(
        symbol= "VENBNB",
        side='BUY',
        type= 'MARKET',
        #timeInForce='FOK',
        quantity= 1.01)
        #price= firstAsk)
print(orderOne)

beginningBalance = client.get_asset_balance(asset='BNB')
print(beginningBalance)

floorTest = math.floor(1.111111 * 100) / 100
print(floorTest)
