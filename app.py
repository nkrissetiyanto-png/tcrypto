import streamlit as st
import plotly.graph_objects as go

from data_loader import load_initial_candles
from ai_engine import AIPredictor
from smartmoney import compute_smart_money
from orderbook_mexc import OrderbookMEXC
from ws_mexc import MEXCWebSocket
from ws_candle_mexc import MEXCCandleWS
from orderbook_mexc import OrderbookMEXC

cs = MEXCCandleWS("BTC_USDT")
cs.start()

st.set_page_config(page_title="Nanang AI Trading Premium", layout="wide")

st.title("🚀 Nanang AI — BTCUSDT Realtime Dashboard (Premium TradingView Style)")

# ==============================================================
# 1) LOAD INITIAL CANDLE DATA
# ==============================================================

df = load_initial_candles("BTCUSDT")

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

df_live = ws.df.copy()

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
st.sidebar.write("Jumlah Bar:", len(df))

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
    #df_live = ws.df if getattr(ws, "df", None) is not None else df
    if len(df_live) > 0:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df_live["time"],
            open=df_live["open"],
            high=df_live["high"],
            low=df_live["low"],
            close=df_live["close"]
        ))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Menunggu data candle dari WebSocket...")

with col2:
    st.subheader("Orderbook Depth")
    st.write("Bids", bids_df.head())
    st.write("Asks", asks_df.head())
