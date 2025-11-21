import requests
import pandas as pd
import streamlit as st


def load_initial_candles(symbol="BTC_USDT"):
    return pd.DataFrame(columns=["time","open","high","low","close","volume"])

