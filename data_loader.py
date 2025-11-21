import requests
import pandas as pd

def load_initial_candles(symbol="BTCUSDT"):
    """
    Ambil historical candle 1 menit dari MEXC.
    MEXC FORMAT: [time, open, high, low, close, volume]
    """

    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval=1m&limit=200"

    try:
        r = requests.get(url, timeout=5)
        raw = r.json()

        # debugging
        print("RAW MEXC:", raw)

        if not isinstance(raw, list):
            return pd.DataFrame()

        df = pd.DataFrame(raw, columns=[
            "time","open","high","low","close","volume",
            "c1","c2","c3","c4","c5","c6"
        ])

        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df[["open","high","low","close","volume"]] = df[["open","high","low","close","volume"]].astype(float)

        df = df[["time","open","high","low","close","volume"]]

        return df

    except Exception as e:
        print("ERROR:", e)
        return pd.DataFrame()
