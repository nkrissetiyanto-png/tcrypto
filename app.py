
import streamlit as st
from websocket_engine import CryptoWebSocket
from data_loader import load_initial_candles
from ai_engine import AIPredictor
from smartmoney import compute_smart_money
from orderbook import OrderbookClient
import plotly.graph_objects as go

st.set_page_config(page_title="Nanang AI Trading Premium", layout="wide")

st.title("🚀 Nanang AI — BTCUSDT Realtime Dashboard (Premium TradingView Style)")

# Load initial data
df = load_initial_candles("BTCUSDT")

# Start websocket
ws = CryptoWebSocket("btcusdt")
ws.start()

# AI model
ai = AIPredictor()

# Orderbook
ob = OrderbookClient("btcusdt")
depth_raw = ob_raw              # response JSON mentah
bids_df = bids                  # dataframe bids
asks_df = asks                  # dataframe asks
price_realtime = df['close'].iloc[-1] if len(df)>0 else None

# =============================
# DEBUG PANEL — CEK DATA MASUK
# =============================
with st.expander("🔍 Debug Data (Klik untuk lihat)", expanded=False):
    st.subheader("Last Raw Depth Data")
    st.json(depth_raw)

    st.subheader("Parsed Bids")
    st.dataframe(bids_df)

    st.subheader("Parsed Asks")
    st.dataframe(asks_df)

    st.subheader("Realtime Price (Terakhir Diterima)")
    st.write(price_realtime)

# Layout
col1, col2 = st.columns([3,1])

with col1:
    st.subheader("Realtime Chart (1m)")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['time'],
        open=df['open'], high=df['high'],
        low=df['low'], close=df['close']
    ))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Orderbook Depth")
    bids, asks = ob.get_depth()
    st.write("Bids", bids.head())
    st.write("Asks", asks.head())

st.subheader("AI Prediction (Next 1m)")
pred = ai.predict(df)
st.metric("Prediction", pred)

