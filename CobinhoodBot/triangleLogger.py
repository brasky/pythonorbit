from datetime import datetime, timezone
local_time = datetime.now(timezone.utc).astimezone()
print(local_time)
from influxdb import InfluxDBClient
dbClient = InfluxDBClient(host='localhost', port=8086)
dbClient.switch_database('test')
def logTriangle(triangle):
    logTime = local_time
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