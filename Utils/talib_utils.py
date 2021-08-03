import ccxt
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
from email_sender import send_email
import time


def convert_number(value):
    return (float(str(float(np.format_float_scientific(value, unique=False, precision=8))).split('e-')[0]))

def get_candle_data(exchange,symbol,interval,limit):
    try:
        exchange = ccxt.binance({'enableRateLimit':True,'options': {'defaultType': 'future',}})
        kline = exchange.fetch_ohlcv(symbol, interval, limit=int(limit))
        df = pd.DataFrame(np.array(kline),columns=['open_time', 'open', 'high', 'low', 'close', 'volume'],dtype='float64')
        """
        op = df['open']
        hi = df['high']
        lo = df['low']
        cl = df['close']
        vl = df['volume']
        timestamps = df['open_time']
        """
        return df
    except Exception as e:
        print(e)