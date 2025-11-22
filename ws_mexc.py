import websocket
import threading
import json
import pandas as pd
from datetime import datetime

class MEXCWebSocket:
    def __init__(self, symbol="BTC_USDT"):
        self.url = "wss://wbs.mexc.com/ws"
        self.symbol = symbol

        # dataframe candle
        self.df = pd.DataFrame(columns=["time","open","high","low","close","volume"])

        # candle aktif (real-time 1 menit)
        self.current_candle = None

    def start(self):
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self):
        ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
        )
        ws.run_forever()

    def on_open(self, ws):
        sub = {
            "method": "sub.deal",
            "params": { "symbol": self.symbol },
            "id": 1
        }
        ws.send(json.dumps(sub))

    def on_message(self, ws, msg):
        data = json.loads(msg)

        if "params" not in data:
            return

        tick = data["params"]

        price = float(tick["deal_price"])
        vol   = float(tick["deal_volume"])
        ts    = int(tick["ts"]) // 1000  # detik

        minute = datetime.utcfromtimestamp(ts).replace(second=0, microsecond=0)

        # jika candle baru (menit berganti)
        if (self.current_candle is None) or (self.current_candle["time"] != minute):

            # simpan candle yang lama ke df
            if self.current_candle is not None:
                self.df.loc[len(self.df)] = self.current_candle

            # mulai candle baru
            self.current_candle = {
                "time": minute,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": vol
            }

        else:
            # update candle berjalan
            self.current_candle["close"] = price
            self.current_candle["high"] = max(self.current_candle["high"], price)
            self.current_candle["low"]  = min(self.current_candle["low"], price)
            self.current_candle["volume"] += vol
