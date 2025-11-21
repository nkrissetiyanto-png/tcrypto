import threading
import websocket
import json
import pandas as pd

class CryptoWebSocket:
    def __init__(self, pair):
        self.url = f"wss://stream.binance.com:9443/ws/{pair}@kline_1m"
        self.last_candle = None
        self.df = pd.DataFrame(columns=["time","open","high","low","close","volume"])
        self.is_running = False  # <-- STATUS UNTUK DASHBOARD

    def on_message(self, ws, msg):
        data = json.loads(msg)
        k = data['k']

        candle = {
            "time": pd.to_datetime(k["T"], unit="ms"),
            "open": float(k["o"]),
            "high": float(k["h"]),
            "low": float(k["l"]),
            "close": float(k["c"]),
            "volume": float(k["v"])
        }

        # Simpan candle terakhir
        self.last_candle = candle

        # Update dataframe realtime
        self.df = pd.concat([self.df, pd.DataFrame([candle])], ignore_index=True)

        # Buat df tetap ringan (max 500 row)
        if len(self.df) > 500:
            self.df = self.df.iloc[-500:]

    def start(self):
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self):
        self.is_running = True

        ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message
        )

        try:
            ws.run_forever()
        except:
            self.is_running = False
