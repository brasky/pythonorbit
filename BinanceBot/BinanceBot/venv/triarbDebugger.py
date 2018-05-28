import math
import decimal
from binance.client import Client
from binance.enums import *
from estimateProfit import *
from organizeCoins import *
from influxdb import InfluxDBClient
from datetime import datetime
from triArb import *
from binance.exceptions import BinanceAPIException
from orbit import *

def Debug(triangle, orderOne, orderTwo, orderThree):
    print("Orderbook changed: Starting Debug")
    print("attempted parameters:", triangle)
    newOrderbook = client.get_orderbook_tickers()
