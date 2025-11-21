
import requests
import pandas as pd

def load_initial_candles(symbol="BTCUSDT", limit=200):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": "1m", "limit": limit}
    r = requests.get(url, params=params)
    data = r.json()
    df = pd.DataFrame(data, columns=[
        'time','open','high','low','close','volume',
        'c1','c2','c3','c4','c5','c6'
    ])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df = df[['time','open','high','low','close','volume']]
    df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].astype(float)
    return df
