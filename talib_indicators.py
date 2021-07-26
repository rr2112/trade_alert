import ccxt
import pandas as pd
import numpy as np
import talib
from datetime import datetime
from email_sender import send_email


def convert_number(value):
    return (float(str(float(np.format_float_scientific(value, unique=False, precision=8))).split('e-')[0]))

def get_indicators(exchange,symbol,interval,limit):
    mail_content = symbol+"Today's stochastic zero cross over - 1h timeframe"+'\n'
    exchange = getattr(ccxt, exchange)()
    kline = exchange.fetch_ohlcv(symbol, interval, limit=int(limit))
    df = pd.DataFrame(np.array(kline),columns=['open_time', 'open', 'high', 'low', 'close', 'volume'],
            dtype='float64')
    op = df['open']
    hi = df['high']
    lo = df['low']
    cl = df['close']
    vl = df['volume']
    timestamps = df['open_time']

    # rsi = talib.RSI(cl.values, timeperiod=14)
    # macd, macdsignal, macdhist = talib.MACD(cl.values, fastperiod=12, slowperiod=26, signalperiod=14)    
    # macd = convert_number(macd[-1])
    # macdsignal = convert_number(macdsignal[-1])
    # ma_50 = convert_number(talib.MA(cl.values, timeperiod=50, matype=0)[-1])
    # ma_100 = convert_number(talib.MA(cl.values, timeperiod=100, matype=0)[-1])
    slowk, slowd = talib.STOCH(hi, lo, cl, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    ts=[datetime.fromtimestamp(int(i/1000)).strftime('%Y-%m-%d %H:%M:%S') for i in timestamps]
    stch_mntm = slowk-slowd
    diff = pd.Series(['positive' if i>=0 else 'Negative' for i in stch_mntm])
    df2 = pd.concat([pd.Series(ts),diff],axis=1)
    for i in range(1,len(df2)):
        if df2.iloc[i-1, 1]!=df2.iloc[i, 1]:
            signal_time=datetime.strptime(df2.iloc[i, 0], '%Y-%m-%d %H:%M:%S')
            today = datetime.today()
            if today.date()==signal_time.date():
                mail_content=mail_content + str(df2.iloc[i, 0] )+ '\n'
    send_email(mail_content)

get_indicators(exchange='binance',symbol='BTC/USDT',interval='1h',limit=100)