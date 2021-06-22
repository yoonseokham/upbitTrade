import pyupbit
import datetime
import os
import sys
import time
import curses
def GetBuyPoint(df,k=0.5):
    larry=list((df["high"]-df["low"])*k+df["close"])[0]
    return larry
seedMoney=3000000
curBtc=0
alreadyBought=False
lastTime=datetime.datetime.now()
df = pyupbit.get_ohlcv("KRW-BTC", interval='day', count=1)
larry=GetBuyPoint(df)

stdscr = curses.initscr()
while True:
    time.sleep(0.2)
    curTime=datetime.datetime.now()
    stdscr.addstr(0, 0, f"""
    보유 btc: {curBtc}
    보유 총 평가: {seedMoney+curBtc*pyupbit.get_current_price('KRW-BTC')}
    보유 KRW: {seedMoney}
    매수할 시점: {larry}
    BTC가격 {pyupbit.get_current_price('KRW-BTC')}
    전고가: {list(df['high'])}
    전저가: {list(df['low'])}
    종가: {list(df['close'])}
    """)
    stdscr.refresh()
    time.sleep(0.2)
    if curTime>=pyupbit.get_ohlcv("KRW-BTC", interval='min', count=1).index[0]:
        time.sleep(0.2)
        if pyupbit.get_current_price('KRW-BTC')>=larry and not alreadyBought:
            #buy all
            time.sleep(0.2)
            buyPrices=pyupbit.get_current_price('KRW-BTC')
            curBtc+=seedMoney/buyPrices
            seedMoney=0
            alreadyBought=True
    else:
        df = pyupbit.get_ohlcv("KRW-BTC", interval='min', count=1)
        larry=GetBuyPoint(df)
        curTime=pyupbit.get_ohlcv("KRW-BTC", interval='min', count=1).index[0]
        alreadyBought=False
        seedMoney+=curBtc*pyupbit.get_current_price('KRW-BTC')
        curBtc=0
