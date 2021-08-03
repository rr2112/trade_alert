import ccxt
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
from Utils.email_sender import send_email
import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print (method.__name__, (te - ts),' - seconds')
        return result
    return timed

def convert_number(value):
    return (float(str(float(np.format_float_scientific(value, unique=False, precision=8))).split('e-')[0]))

@timeit
def get_indicators(exchange,symbol,interval,limit):
    pair_mail_content=str()
    # exchange = getattr(ccxt, exchange)()
    try:
        exchange = ccxt.binance({'enableRateLimit':True,'options': {'defaultType': 'future',}})
        kline = exchange.fetch_ohlcv(symbol, interval, limit=int(limit))
        df = pd.DataFrame(np.array(kline),columns=['open_time', 'open', 'high', 'low', 'close', 'volume'],dtype='float64')
        op = df['open']
        hi = df['high']
        lo = df['low']
        cl = df['close']
        vl = df['volume']
        timestamps = df['open_time']

        slowk, slowd = talib.STOCH(hi, lo, cl, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        ts=[datetime.fromtimestamp(int(i/1000)).strftime('%Y-%m-%d %H:%M:%S') for i in timestamps]
        stch_mntm = slowk-slowd
        diff = pd.Series(['positive' if i>=0 else 'Negative' for i in stch_mntm])
        df2 = pd.concat([pd.Series(ts),diff],axis=1)
        # print(df2.to_string())
        for i in range(1,len(df2)):
            if df2.iloc[i-1, 1]!=df2.iloc[i, 1]:
                signal_time=datetime.strptime(df2.iloc[i, 0], '%Y-%m-%d %H:%M:%S')
                # today = datetime.today()
                # if today.date()==signal_time.date():
                if signal_time>=datetime.now()-timedelta(days=2):
                    pair_mail_content+= str(df2.iloc[i, 0] )+ '\n'
                    print(pair_mail_content)
        return pair_mail_content
    except Exception as e:
        print(e)


@timeit
def trigger_email():
    mail_content = ''
    all_futures_pairs = ('1000SHIB/USDT','1INCH/USDT','AAVE/USDT','ADA/USDT','AKRO/USDT','ALGO/USDT','ALICE/USDT','ALPHA/USDT','ANKR/USDT','ATOM/USDT','AVAX/USDT','AXS/USDT','BAKE/USDT','BAL/USDT','BAND/USDT','BAT/USDT','BCH/USDT','BEL/USDT','BLZ/USDT','BNB/USDT','BTCDOM/USDT','BTS/USDT','BTT/USDT','BZRX/USDT','CELR/USDT','CHR/USDT','CHZ/USDT','COMP/USDT','COTI/USDT','CRV/USDT','CTK/USDT','CVC/USDT','DASH/USDT','DEFI/USDT','DENT/USDT','DGB/USDT','DODO/USDT','DOGE/USDT','DOT/USDT','EGLD/USDT','ENJ/USDT','EOS/USDT','ETC/USDT','ETH/USDT','FIL/USDT','FLM/USDT','GRT/USDT','GTC/USDT','HBAR/USDT','HNT/USDT','HOT/USDT','ICP/USDT','ICX/USDT','IOST/USDT','IOTA/USDT','KAVA/USDT','KEEP/USDT','KNC/USDT','KSM/USDT','LINA/USDT','LINK/USDT','LIT/USDT','LRC/USDT','LTC/USDT','LUNA/USDT','MANA/USDT','MATIC/USDT','MKR/USDT','MTL/USDT','NEAR/USDT','NEO/USDT','NKN/USDT','OCEAN/USDT','OGN/USDT','OMG/USDT','ONE/USDT','ONT/USDT','QTUM/USDT','REEF/USDT','REN/USDT','RLC/USDT','RSR/USDT','RUNE/USDT','RVN/USDT','SAND/USDT','SC/USDT','SFP/USDT','SKL/USDT','SNX/USDT','SOL/USDT','SRM/USDT','STMX/USDT','STORJ/USDT','SUSHI/USDT','THETA/USDT','TLM/USDT','TOMO/USDT','TRX/USDT','UNFI/USDT','UNI/USDT','VET/USDT','WAVES/USDT','XEM/USDT','XLM/USDT','XMR/USDT','XRP/USDT','XTZ/USDT','YFII/USDT','YFI/USDT','ZEC/USDT','ZEN/USDT','ZIL/USDT','ZRX/USDT')
    for pair in all_futures_pairs:
        pair_mail_content = get_indicators(exchange='binance',symbol=pair,interval='1d',limit=100)
        if len(pair_mail_content)>0:
            mail_content += pair + " last 2 hours- stochastic zero cross over - 1d timeframe"+'\n'+pair_mail_content
    if len(mail_content)>0:
        print(mail_content)
        send_email(mail_content)
    else:
        print("no crossover in last 2 hours")
    

# trigger_email()
get_indicators(exchange='binance',symbol='SAND/USDT',interval='1h',limit=400)