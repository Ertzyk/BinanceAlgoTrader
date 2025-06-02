import pandas as pd
import time
from config import client

def fetch_data(symbol, interval, lookback):
    candles = client.get_klines(symbol=symbol, interval=interval, limit=lookback)
    df = pd.DataFrame(candles, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'trades',
        'taker_base_volume', 'taker_quote_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    return df[['timestamp', 'close']]

def calculate_moving_averages(df, short_window, long_window):
    df['SMA_short'] = df['close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['close'].rolling(window=long_window).mean()
    return df

def trade_logic(df, symbol, quantity):
    if df['SMA_short'].iloc[-1] > df['SMA_long'].iloc[-1] and df['SMA_short'].iloc[-2] <= df['SMA_long'].iloc[-2]:
        print(f"Bought {quantity} {symbol}")
    elif df['SMA_short'].iloc[-1] < df['SMA_long'].iloc[-1] and df['SMA_short'].iloc[-2] >= df['SMA_long'].iloc[-2]:
        print(f"Sold {quantity} {symbol}")

def main():
    symbol = 'BTCUSDT'
    interval = '1m'
    lookback = 50
    short_window = 10
    long_window = 30
    quantity = 0.001

    while True:
        try:
            df = fetch_data(symbol, interval, lookback)
            print(df)
            df = calculate_moving_averages(df, short_window, long_window)
            print(df)
            time.sleep(3600)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()