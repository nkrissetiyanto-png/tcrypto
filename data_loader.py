import requests
import pandas as pd
import streamlit as st


def load_initial_candles(symbol="BTCUSDT"):
    symbol = symbol.replace("-", "").replace("_", "").upper()
    #symbol = f"{symbol[:-4]}_{symbol[-4:]}"   # BTCUSDT → BTC_USDT

    url = f"https://api.mexc.com/api/v2/market/kline?symbol={symbol}&interval=1m&limit=200"

    r = requests.get(url, timeout=10)
    raw = r.json()

    # Tampilkan di UI Streamlit (bukan print)
    with st.expander("📄 RAW RESPONSE dari MEXC"):
        st.json(raw)

    if "data" not in raw:
        st.error("MEXC ERROR: API tidak mengembalikan data candle!")
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
    df[["open","high","low","close","volume"]] = df[["open","high","low","close","volume"]].astype(float)

    return df
