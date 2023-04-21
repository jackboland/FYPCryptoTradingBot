import pprint, sys, time, json, talib, numpy
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
from .basebot import buy, sell, backtestbuy, backtestsell
from .smabot import get_sma

def get_ema(closes, period):
    # calculate the exponential moving average
    multiplier = 2 / (period + 1)
    ema_value = sum(closes[:period]) / period
    
    for close in closes[period:]:
        ema_value = (close * multiplier) + (ema_value * (1 - multiplier))
        
    return ema_value

def emacalculation(candlecloses, backtesting):
    closes_20_old = candlecloses[-21:]
    closes_20_old.pop()
    closes_20_new = candlecloses[-20:]
    closes_100 = candlecloses
    ema20 = [get_ema(closes_20_old, 20), get_ema(closes_20_new, 20)]
    sma100 = get_sma(closes_100, 100)

    if sma100 > 0: 
        if ema20[1] > sma100 and ema20[0] < sma100:
            from .basebot import in_position
            if in_position:
                print("Golden Cross! Possible bull market ahead, good time to sell!")
                if backtesting == 0:
                    sell()
                elif backtesting == 1:
                    backtestsell(candlecloses[-1])
            else: 
                print("Golden Cross! Now may have been a good time to sell, but none is owned!")
        
        elif ema20[1] < sma100 and ema20[0] > sma100:
            from .basebot import in_position
            if in_position:
                print("Death cross! Now may have been a good time to buy, but some is already owned!")
            else: 
                print("Death cross! Possible bear market ahead, good time to buy!")
                if backtesting == 0:
                    buy()
                elif backtesting == 1:
                    backtestbuy(candlecloses[-1])
                



