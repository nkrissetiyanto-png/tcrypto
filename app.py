import streamlit as st
import plotly.graph_objects as go

from websocket_engine import CryptoWebSocket
from data_loader import load_initial_candles
from ai_engine import AIPredictor
from smartmoney import compute_smart_money
from orderbook import OrderbookClient

st.set_page_config(page_title="Nanang AI Trading Premium", layout="wide")

st.title("🚀 Nanang AI — BTCUSDT Realtime Dashboard (Premium TradingView Style)")

# ==============================================================
# 1) LOAD INITIAL DATA + START WEBSOCKET
# ==============================================================

df = load_initial_candles("BTCUSDT")

ws = CryptoWebSocket("btcusdt")
ws.start()  # websocket live

ai = AIPredictor()

# ==============================================================
# 2) ORDERBOOK (REST)
# ==============================================================
self.is_running = True

st.sidebar.write("📡 WebSocket Connected:", ws.is_running)
st.sidebar.write("📈 Last Price:", price_realtime)
st.sidebar.write("🧊 Bids Count:", len(bids_df))
st.sidebar.write("🔥 Asks Count:", len(asks_df))

ob = OrderbookClient("btcusdt")
depth_raw, bids_df, asks_df = ob.get_depth()

price_realtime = df['close'].iloc[-1] if len(df)>0 else None

# ==============================================================
# 3) DEBUG PANEL — CEK APAKAH DATA MASUK
# ==============================================================
with st.expander("🔍 Debug Data (Klik untuk lihat)", expanded=False):
    st.subheader("Last Raw Depth Data")
    st.json(depth_raw)

    st.subheader("Parsed Bids")
    st.dataframe(bids_df)

    st.subheader("Parsed Asks")
    st.dataframe(asks_df)

# ==============================================================
# 4) LAYOUT — CHART + ORDERBOOK
# ==============================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Realtime Chart (1m)")

    # update df from websocket if exists
    df_live = ws.df if ws.df is not None else df

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df_live["time"],
        open=df_live["open"],
        high=df_live["high"],
        low=df_live["low"],
        close=df_live["close"]
    ))
    fig.update_layout(height=500, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Orderbook Depth")
    st.write("Bids", bids_df.head())
    st.write("Asks", asks_df.head())

# =============================================================
