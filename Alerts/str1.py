from .Utils.talib_utils import get_candle_data

df = get_candle_data('binance','ALICE/USDT','4h',100)

print(df.to_string())