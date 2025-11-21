import streamlit as st
import plotly.graph_objects as go

f#rom websocket_engine import CryptoWebSocket
from data_loader import load_initial_candles
from ai_engine import AIPredictor
from smartmoney import compute_smart_money
#from orderbook import OrderbookClient
#from orderbook_ws import OrderbookWebSocket
from orderbook_mexc import OrderbookMEXC
from ws_mexc import MEXCWebSocket

#ob_ws = OrderbookWebSocket("btcusdt")
#ob_ws.start()


# gunakan ini untuk display
#bids_df = ob_ws.bids
#asks_df = ob_ws.asks

st.set_page_config(page_title="Nanang AI Trading Premium", layout="wide")

st.title("🚀 Nanang AI — BTCUSDT Realtime Dashboard (Premium TradingView Style)")

# ==============================================================
# 1) LOAD INITIAL CANDLE DATA
# ==============================================================

df = load_initial_candles("BTC_USDT")

# ==============================================================
# 2) START WEBSOCKET
# ==============================================================

#ws = CryptoWebSocket("btcusdt")
#ws.start()  # websocket berjalan di background

ai = AIPredictor()

# ==============================================================
# 3) ORDERBOOK REST API
# ==============================================================

#ob = OrderbookClient("btcusdt")
#depth_raw, bids_df, asks_df = ob.get_depth()
ws = MEXCWebSocket("BTC_USDT")
ws.start()

ob = OrderbookMEXC("BTC_USDT")
depth_raw, bids_df, asks_df = ob.get_depth()

price_realtime = df['close'].iloc[-1] if len(df) > 0 else None

# ==============================================================
# 4) SIDEBAR STATUS PANEL
# ==============================================================

st.sidebar.write("📡 WebSocket Connected:", getattr(ws, "is_running", True))
st.sidebar.write("📈 Last Price:", price_realtime)
st.sidebar.write("🧊 Bids Count:", len(bids_df))
st.sidebar.write("🔥 Asks Count:", len(asks_df))

# ==============================================================
# 5) DEBUG PANEL
# ==============================================================

with st.expander("🔍 Debug Data (Klik untuk lihat)", expanded=False):
    st.subheader("Last Raw Depth Data")
    st.json(depth_raw)

    st.subheader("Parsed Bids")
    st.dataframe(bids_df)

    st.subheader("Parsed Asks")
    st.dataframe(asks_df)

# ==============================================================
# 6) LAYOUT — CHART & ORDERBOOK
# ==============================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Realtime Chart (1m)")

    # Ambil data dari websocket bila tersedia
    df_live = ws.df if getattr(ws, "df", None) is not None else df

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
