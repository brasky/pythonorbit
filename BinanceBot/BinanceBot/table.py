from binance.client import Client
client = Client(parameters.apiKey, parameters.apiSecret)
print = str(client.get_ticker(symbol="LTCBTC"))
