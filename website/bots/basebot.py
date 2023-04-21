import json
import pprint
import sys
import time

import numpy
import talib
from flask import current_app as app
from flask_login import current_user
from kraken.futures import Market, Trade
from kraken.futures import User as KrakenUser

from .. import db
from ..models import BacktestTransactions, CandleData, Transactions, User


def create_user():
    with app.app_context():
        key = User.query.filter_by(email=current_user.email).first().api_key
        secret = User.query.filter_by(email=current_user.email).first().api_secret
        user = KrakenUser(key=key, secret=secret, sandbox=True)
    return user

def get_wallet_balance():
    return create_user().get_wallets()

def create_trade():
    with app.app_context():
        key = User.query.filter_by(email=current_user.email).first().api_key
        secret = User.query.filter_by(email=current_user.email).first().api_secret
        trade = Trade(key=key, secret=secret, sandbox=True)
    return trade

in_position = False

market = Market()

tradesize = 1

backtesting_wallet = 500000

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

    # Calculate the cutoff timestamp for the 30th most recent entry
    cutoff_entry = CandleData.query.order_by(CandleData.timestamp.desc()).offset(99).first()
    if cutoff_entry:
        cutoff_time = cutoff_entry.timestamp
        # Delete all entries older than the 30th most recent entry
        db.session.query(CandleData).filter(CandleData.timestamp < cutoff_time).delete()
        db.session.commit()

def read_last_candle_time():
    data = CandleData.query.order_by(CandleData.id.desc())
    temp = data.first()
    if isinstance(temp, CandleData):
        return temp.timestamp
    else:
        return 1

def buy():
    trade = create_trade()
    trade.create_order(orderType='mkt', side='buy', size=0.05, symbol='pf_xbtusd')
    print("this is the buy function!")

def sell():
    trade = create_trade()
    trade.create_order(orderType='mkt', side='sell', size=0.05, symbol='pf_xbtusd')
    print("this is the sell function!")

def backtestbuy(candleprice):
    global backtesting_wallet
    global in_position
    backtesting_wallet = backtesting_wallet - candleprice
    new_data = BacktestTransactions(information = "Bought for " + str(candleprice) + "! Wallet balance: " + str(backtesting_wallet))
    db.session.add(new_data)
    db.session.commit()
    in_position= True

def backtestsell(candleprice):
    global backtesting_wallet
    global in_position
    backtesting_wallet = backtesting_wallet + candleprice
    new_data = BacktestTransactions(information = "Sold for " + str(candleprice) + "! Wallet balance: " + str(backtesting_wallet))
    db.session.add(new_data)
    db.session.commit()
    in_position= False

def reset_backtesting_data():
    global in_position
    global backtesting_wallet
    backtesting_wallet = 500000
    in_position = False
    num_rows_deleted = db.session.query(BacktestTransactions).delete()
    db.session.commit()

