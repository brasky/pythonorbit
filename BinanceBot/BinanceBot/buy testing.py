import  parameters
import time
from binance.client import Client
client = Client(parameters.apiKey, parameters.apiSecret)
orderOne = client.create_test_order(
        symbol= "BNBBTC",
        side='BUY',
        type= 'MARKET',
        #timeInForce='FOK',
        quantity= 1)
        #price= firstAsk)
print(orderOne)