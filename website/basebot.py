from kraken.futures import Market, User, Trade, Funding
import pprint, sys, time, json, talib, numpy
from .models import CandleData
from . import db

key = '0tU3AYdaDJ53uCOFEN08gROOLmoDvRi2riiBcOVX+AXwR94fpWfTXOUz'
secret = 'm81X/6C5aTg83FKXNGzrDOvMraUIOLxXjtbxDqFd6Imm5CUDA1C6T4x7XhG6GAfSW8lV528DwjoSA/V4Rnr9O1Bn'

market = Market()

user = User(key=key, secret=secret, sandbox=True)

def get_candle_close(app):
    with app.app_context():
        try:
            while True:
                response = market.get_ohlc(tick_type='trade', symbol='PF_XBTUSD', resolution='1m')
                close = int(float(response["candles"][0]["close"]))
                timestamp = int(float(response["candles"][0]["time"]))
                print(close)
                print (timestamp)
                concatdata = str(close) + " " + str(timestamp)
                add_candle_to_db(concatdata)
                time.sleep(60)
        except KeyboardInterrupt:
            sys.exit(0)

def add_candle_to_db(candle):
    temp = read_last_candle_time()
    close, timestamp = candle.split(' ')
    if temp != int(timestamp):
        new_data = CandleData(close=close, timestamp=timestamp)
        db.session.add(new_data)
        db.session.commit()

def read_last_candle_time():
    data = CandleData.query.order_by(CandleData.id.desc())
    temp = data.first()
    if isinstance(temp, CandleData):
        return temp.timestamp
    else:
        return 1
