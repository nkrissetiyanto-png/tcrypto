import websocket
import json
import pandas as pd
import threading


class MEXCCandleWS:
    def __init__(self, symbol="BTC_USDT"):
        self.url = f"wss://wbs.mexc.com/ws"
        self.symbol = symbol

        self.df = pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])
        self.lock = threading.Lock()

    # ---------------------------------------
    def start(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    # ---------------------------------------
    def _run(self):
        ws = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message
        )
        ws.run_forever()

    # ---------------------------------------
    def _on_open(self, ws):
        sub_msg = {
            "method": "SUBSCRIPTION",
            "params": [f"spot@public.kline.v3.api@{self.symbol}@Min1"]
        }
        ws.send(json.dumps(sub_msg))

    # ---------------------------------------
    def _on_message(self, ws, message):
        try:
            msg = json.loads(message)

            if "data" not in msg:
                return

            k = msg["data"]["k"]

            new_row = {
                "time": pd.to_datetime(k["t"], unit="ms"),
                "open": float(k["o"]),
                "high": float(k["h"]),
                "low": float(k["l"]),
                "close": float(k["c"]),
                "volume": float(k["v"]),
            }

            with self.lock:
                self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

                # Simpan maksimal 200 candle biar ringan
                if len(self.df) > 200:
                    self.df = self.df.iloc[-200:]

        except Exception as e:
            print("WS Candle Error:", e)
