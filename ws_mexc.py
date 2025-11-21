import websocket
import json
import threading
import pandas as pd

class MEXCWebSocket:
    def __init__(self, symbol="BTC_USDT"):
        self.symbol = symbol
        self.url = "wss://wbs.mexc.com/ws"
        self.last_candle = None
        self.df = pd.DataFrame(columns=["time","open","high","low","close","volume"])

    def _on_message(self, ws, msg):
        data = json.loads(msg)

        if "data" not in data:
            return

        k = data["data"]

        candle = {
            "time": pd.to_datetime(k["t"], unit='ms'),
            "open": float(k["o"]),
            "high": float(k["h"]),
            "low": float(k["l"]),
            "close": float(k["c"]),
            "volume": float(k["v"]),
        }

        self.last_candle = candle
        self.df = pd.concat([self.df, pd.DataFrame([candle])], ignore_index=True)

    def _on_open(self, ws):
        sub = {
            "method": "SUBSCRIPTION",
            "params": [f"spot@public.kline.v3.api@{self.symbol}@Min1"]
        }
        ws.send(json.dumps(sub))

    def start(self):
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        ws = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message
        )
        ws.run_forever()
