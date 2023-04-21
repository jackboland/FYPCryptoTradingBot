import pprint, sys, time, json, talib, numpy
from .basebot import buy, sell, backtestbuy, backtestsell

def macdcalculation(candlecloses, backtesting):
    SLOW_PERIOD = 26
    FAST_PERIOD = 12
    SIGNAL_PERIOD = 9

    np_closes = numpy.array(candlecloses)
    macd, signal_line, histogram = talib.MACD(np_closes, fastperiod=FAST_PERIOD, slowperiod=SLOW_PERIOD, signalperiod=SIGNAL_PERIOD)
    last_histogram = histogram[-1]

    if last_histogram > 0:
        from .basebot import in_position
        if in_position:
            print("MACD is positive, good time to hold or sell!")
        else:
            print("MACD is positive, good time to buy!")
            if backtesting == 0:
                buy()
            elif backtesting == 1:
                backtestbuy(candlecloses[-1])

    if last_histogram < 0:
        from .basebot import in_position
        if in_position:
            print("MACD is negative, good time to sell!")
            if backtesting == 0:
                sell()
            elif backtesting == 1:
                backtestsell(candlecloses[-1])
        else:
            print("MACD is negative, but none is owned!")