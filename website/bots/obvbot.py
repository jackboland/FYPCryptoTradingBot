import pprint, sys, time, json, talib, numpy
import pandas as pd
from .basebot import buy, sell, backtestbuy, backtestsell

def obvcalculation(candlecloses, backtesting):
    np_closes = numpy.array(candlecloses)
    volumes = numpy.where(np_closes >= numpy.roll(np_closes, 1), 1, -1)[1:]
    obv = pd.Series(volumes, index=candlecloses[1:]).cumsum()
    obv = pd.concat([pd.Series([0], index=[candlecloses[0]]), obv])
    obv_slope = obv.diff().iloc[-1]
    print(obv_slope)

    # Implement your logic for buying and selling based on the OBV slope here
    if obv_slope > 0:
        from .basebot import in_position
        if in_position:
            print("Increasing OBV slope, good time to sell!")
            if backtesting == 0:
                sell()
            elif backtesting == 1:
                backtestsell(candlecloses[-1])
        else: 
            print("Increasing OBV slope, but none is owned!")
    
    if obv_slope < 0:
        from .basebot import in_position
        if in_position:
            print("Decreasing OBV slope, but some is already owned!")
        else: 
            print("Decreasing OBV slope, good time to buy!")
            if backtesting == 0:
                buy()
            elif backtesting == 1:
                backtestbuy(candlecloses[-1])