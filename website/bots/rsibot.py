import pprint, sys, time, json, talib, numpy
from .basebot import buy, sell, backtestbuy, backtestsell

def rsicalculation(candlecloses, backtesting):
    
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30

    np_closes = numpy.array(candlecloses)
    rsi = talib.RSI(np_closes, RSI_PERIOD)
    last_rsi = rsi[-1]
    print(last_rsi)

    if last_rsi > RSI_OVERBOUGHT:
        from .basebot import in_position
        if in_position:
            print("Symbol overbought, good time to sell!")
            if backtesting == 0:
                sell()
            elif backtesting == 1:
                backtestsell(candlecloses[-1])
        else: 
            print("Symbol overbought, but none is owned!")
    
    if last_rsi < RSI_OVERSOLD:
        from .basebot import in_position
        if in_position:
            print("Symbol oversold, but some is already owned!")
        else: 
            print("Symbol oversold, good time to buy!")
            if backtesting == 0:
                buy()
            elif backtesting == 1:
                backtestbuy(candlecloses[-1])
            
    
