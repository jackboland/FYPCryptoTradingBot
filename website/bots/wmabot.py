import pprint, sys, time, json, talib, numpy
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
from .basebot import buy, sell, backtestbuy, backtestsell
from .smabot import get_sma

def get_wma(closes, period):
    # calculate the weighted moving average
    weights = list(range(1, period+1))
    weights_sum = sum(weights)
    weights_list = weights[::-1] # reverse the weights list for ease of use
    
    wma_value = sum([close * weight for close, weight in zip(closes[-period:], weights_list)]) / weights_sum
    
    return wma_value


def wmacalculation(candlecloses, backtesting):
    closes_20_old = candlecloses[-21:]
    closes_20_old.pop()
    closes_20_new = candlecloses[-20:]
    closes_100 = candlecloses
    wma20 = [get_wma(closes_20_old, 20), get_wma(closes_20_new, 20)]
    sma100 = get_sma(closes_100, 100)

    if sma100 > 0: 
        if wma20[1] > sma100 and wma20[0] < sma100:
            from .basebot import in_position
            if in_position:
                print("Golden Cross! Possible bull market ahead, good time to sell!")
                if backtesting == 0:
                    sell()
                elif backtesting == 1:
                    backtestsell(candlecloses[-1])
            else: 
                print("Golden Cross! Now may have been a good time to sell, but none is owned!")
        
        elif wma20[1] < sma100 and wma20[0] > sma100:
            from .basebot import in_position
            if in_position:
                print("Death cross! Now may have been a good time to buy, but some is already owned!")
            else: 
                print("Death cross! Possible bear market ahead, good time to buy!")
                if backtesting == 0:
                    buy()
                elif backtesting == 1:
                    backtestbuy(candlecloses[-1])
                



