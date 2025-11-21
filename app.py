import streamlit as st
import plotly.graph_objects as go

# HANYA MEXC — jangan import Binance lagi
from data_loader import load_initial_candles
from ai_engine import AIPredictor
from smartmoney import compute_smart_money
from orderbook_mexc import OrderbookMEXC
from ws_mexc import MEXCWebSocket

st.set_page_config(page_title="Nanang AI Trading Premium", layout="wide")

st.title("🚀 Nanang AI — BTC_USDT Realtime Dashboard (MEXC Feed)")

# 1) Load historical candle MEXC
df = load_initial_candles("BTC_USDT")

# 2) WebSocket MEXC
ws = MEXCWebSocket("BTC_USDT")
ws.start()

# 3) Orderbook
ob = OrderbookMEXC("BTC_USDT")
depth_raw, bids_df, asks_df = ob.get_depth()

# 4) Price realtime
price_realtime = df['close'].iloc[-1] if len(df) > 0 else None

# 5) UI - debug
with st.expander("Debug"):
    st.json(depth_raw)
