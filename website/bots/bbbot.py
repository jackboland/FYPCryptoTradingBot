import pprint, sys, time, json, talib, numpy
from .basebot import buy, sell, backtestbuy, backtestsell

from .smabot import get_sma

def bollingerbandcalculation(candlecloses, backtesting):
    
    np_closes = numpy.array(candlecloses)

    ma = talib.SMA(np_closes, 20)

    std = numpy.std(candlecloses[-20:])

    upper_band = ma + 2*std
    lower_band = ma - 2*std

    last_close = candlecloses[-1]
    last_ma = ma[-1]
    
    if last_close > upper_band[-1]:
        from .basebot import in_position
        if in_position:
            print("Symbol overbought, good time to sell!")
            if backtesting == 0:
                sell()
            elif backtesting == 1:
                backtestsell(last_close)
        else:
            print("Symbol overbought, but none is owned!")

    elif last_close < lower_band[-1]:
        from .basebot import in_position
        if in_position:
            print("Symbol oversold, but some is already owned!")
        else:
            print("Symbol oversold, good time to buy!")
            if backtesting == 0:
                buy()
            elif backtesting == 1:
                backtestbuy(last_close)