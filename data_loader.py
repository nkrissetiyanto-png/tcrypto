import requests
import pandas as pd


def normalize_symbol(symbol: str):
    symbol = symbol.replace("-", "").replace("_", "")
    base = symbol[:-4]
    quote = symbol[-4:]
    return f"{base}_{quote}".upper()


def load_initial_candles(symbol="BTCUSDT"):
    symbol = normalize_symbol(symbol)

    url = f"https://api.mexc.com/api/v2/market/kline?symbol={symbol}&interval=1m&limit=200"

    try:
        r = requests.get(url, timeout=10)
        raw = r.json()

        # DEBUG
        print("RAW RESPONSE:", raw)

        if "data" not in raw or len(raw["data"]) == 0:
            print("⚠ ERROR — MEXC returned empty data")
            return pd.DataFrame()

        rows = raw["data"]

        df = pd.DataFrame(rows)
        df = df.rename(columns={
            "t": "time",
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume"
        })

        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df[["open","high","low","close","volume"]] = \
            df[["open","high","low","close","volume"]].astype(float)

        return df[["time","open","high","low","close","volume"]]

    except Exception as e:
        print("⚠ ERROR data_loader:", e)
        return pd.DataFrame()
