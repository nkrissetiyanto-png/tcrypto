import requests
import pandas as pd
import streamlit as st

def load_initial_candles(symbol="BTC_USDT"):
    """
    Load historical 1-minute candles dari endpoint spot MEXC yang resmi & stabil.
    """

    url = f"https://api.mexc.com/api/v3/depth?symbol={symbol}&limit=20"

    try:
        r = requests.get(url, timeout=8)
        raw = r.json()

        # debug friendly (optional)
        with st.expander("RAW Candle API Response"):
            st.json(raw)

        if "data" not in raw:
            st.error("MEXC tidak mengembalikan field 'data'.")
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

    except Exception as e:
        st.error(f"ERROR data_loader: {e}")
        return pd.DataFrame()
