import  parameters
import math
import time
from binance.client import Client
client = Client(parameters.apiKey, parameters.apiSecret)
bnbBal = float(client.get_asset_balance(asset='BNB')['free'])
ordertwoQty = math.floor((bnbBal) * 100)/100
print(ordertwoQty)
orderOne = client.create_test_order(
    symbol="VENBTC",
    side='SELL',
    type='MARKET',
    quantity=1000.1
    )

print(orderOne)

