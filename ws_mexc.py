import websocket
import json
import threading
import pandas as pd

class MEXCWebSocket:
    def __init__(self, symbol="BTC_USDT"):
        self.symbol = symbol.lower()
        self.last_candle = None
        self.url = f"wss://wbs.mexc.com/ws"

    def _on_message(self, ws, message):
        data = json.loads(message)

        if "c" not in data: 
            return

        k = data["c"]

        self.last_candle = {
            "time": pd.to_datetime(k["T"], unit="ms"),
            "open": float(k["o"]),
            "high": float(k["h"]),
            "low": float(k["l"]),
            "close": float(k["c"]),
            "volume": float(k["v"]),
        }

    def _on_open(self, ws):
        sub_msg = {
            "method": "SUBSCRIPTION",
            "params": [f"spot@public.kline.v3.api@{self.symbol}@Min1"]
        }
        ws.send(json.dumps(sub_msg))

    def start(self):
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self):
        ws = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message
        )
        ws.run_forever()
