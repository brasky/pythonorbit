from datetime import datetime, timezone
from influxdb import InfluxDBClient
dbClient = InfluxDBClient(host='localhost', port=8086)
dbClient.switch_database('test')
def logTriangle(triangle):
    logTime = datetime.now(timezone.utc).astimezone()
    print(logTime)
    loggingInput = [
        {
        "measurement": "profitability",
        "tags": {
            "coinName1": triangle['coin1'],
            "coinName2": triangle['coin2']
        },
        "time": logTime,
        "fields": {
            "profitability": triangle['profit'],
            "maxThroughput": triangle['maxThru']
        }
        }
    ]
    if dbClient.write_points(loggingInput) == True:
        return 'Triangle Logged Successfully'

def logTrade(order):
    logtime = datetime.now(timezone.utc).astimezone()
    loggingInput = [
        {
        "measurement": "execution",
        "tags": {
            "id": order['result']['order']['id'],
            "trading_pair_id": order['result']['order']['trading_pair_id'],
            "side": order['result']['order']['side'],
            "type": order['result']['order']['type']
        },
        "time": logtime,
        "fields": {
            "price": order['result']['order']['price'],
            "size": order['result']['order']['size'],
            "filled": order['result']['order']['filled'],
            "state": order['result']['order']['state']
        }
        }
    ]
    if dbClient.write_points(loggingInput) == True:
        return 'Trade Logged Successfully'