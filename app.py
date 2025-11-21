import streamlit as st
import plotly.graph_objects as go

from data_loader import load_initial_candles   # REST klines
from ai_engine import AIPredictor
from smartmoney import compute_smart_money
from orderbook_mexc import OrderbookMEXC       # REST orderbook
from ws_mexc import MEXCWebSocket              # LIVE websocket ticker


# ==============================================================
# STREAMLIT PAGE CONFIG
# ==============================================================

st.set_page_config(page_title="Nanang AI Trading Premium", layout="wide")
st.title("🚀 Nanang AI — BTCUSDT Realtime Dashboard (Premium TradingView Style)")


# ==============================================================
# 1) LOAD INITIAL CANDLE DATA (REST API)
# ==============================================================

# ❗ IMPORTANT: MEXC REST uses symbol WITHOUT underscore → BTCUSDT
df = load_initial_candles("BTCUSDT")

with st.expander("📄 Debug DF Candle (REST)"):
    st.write(df)
    st.write("Jumlah Bar:", len(df))

if df.empty:
    st.error("❌ REST API candle (klines) dari MEXC kosong! Chart tidak bisa ditampilkan.")
    st.stop()


# ==============================================================
# 2) START LIVE WEBSOCKET (MEXC)
# ==============================================================

ws = MEXCWebSocket("BTC_USDT")   # websocket FORMAT pakai underscore
ws.start()


# ==============================================================
# 3) ORDERBOOK (REST API)
# ==============================================================

ob = OrderbookMEXC("BTC_USDT")
depth_raw, bids_df, asks_df = ob.get_depth()

# harga realtime fallback dari REST saja
price_realtime = df['close'].iloc[-1]


# ==============================================================
# 4) SIDEBAR STATUS PANEL
# ==============================================================

st.sidebar.subheader("Status Monitor")
st.sidebar.write("📡 WebSocket Connected:", getattr(ws, "is_running", True))
st.sidebar.write("📈 Last Price:", price_realtime)
st.sidebar.write("🧊 Bids Count:", len(bids_df))
st.sidebar.write("🔥 Asks Count:", len(asks_df))


# ==============================================================
# 5) DEBUG PANEL — LIHAT DATA RAW
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


# ================= CHART =================
with col1:

    st.subheader("📊 Realtime Chart (1m)")

    # Websocket MEXC tidak mengirim candle → gunakan REST candle (df)
    df_live = df

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df_live["time"],
        open=df_live["open"],
        high=df_live["high"],
        low=df_live["low"],
        close=df_live["close"],
        name="price"
    ))

    fig.update_layout(
        height=500,
        template="plotly_dark",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)


# ================= ORDERBOOK =================
with col2:

    st.subheader("📘 Orderbook Depth (MEXC)")

    st.write("Bids (Buy Orders)")
    st.dataframe(bids_df.head())

    st.write("Asks (Sell Orders)")
    st.dataframe(asks_df.head())


# ==============================================================
# 7) AI PREDICTION
# ==============================================================

st.subheader("🤖 AI Prediction (Next 1m)")
ai = AIPredictor()

try:
    pred = ai.predict(df_live)
    st.metric("Prediction", pred)
except Exception as e:
    st.error(f"AI Error: {e}")
