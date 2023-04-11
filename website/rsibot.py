import pprint, sys, time, json, talib, numpy
from . import basebot

def rsicalculation(candlecloses):

    in_position = False

    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30

    print(candlecloses)
    np_closes = numpy.array(candlecloses)
    print(np_closes)
    rsi = talib.RSI(np_closes, RSI_PERIOD)
    last_rsi = rsi[-1]
    rsi = talib.RSI(np_closes, RSI_PERIOD)

    if last_rsi > RSI_OVERBOUGHT:
        if in_position:
            print("Symbol overbought, good time to sell!")
            #CONFIDENCE LEVEL
            #CONFIRM SELL
            order_succeeded = True
            #SELL
            if order_succeeded:
                in_position= False
        else: 
            print("Symbol overbought, but none is owned!")
    
    if last_rsi < RSI_OVERSOLD:
        if in_position:
            print("Symbol oversold, good time to buy!")
            #CONFIDENCE LEVEL
            #CONFIRM BUY
            order_succeeded = True
            #BUY
            if order_succeeded:
                in_position= True
        else: 
            print("Symbol oversold, but some is already owned!")
    
    print(rsi)