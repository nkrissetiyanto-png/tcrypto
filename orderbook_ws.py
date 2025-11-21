import websocket
import threading
import json
import pandas as pd

class OrderbookWebSocket:
    def __init__(self, symbol="btcusdt"):
        self.url = f"wss://stream.binance.com/ws/btcusdt@kline_1s"
        self.bids = pd.DataFrame(columns=["price", "qty"])
        self.asks = pd.DataFrame(columns=["price", "qty"])

    #"wss://stream.binance.com:9443/ws/btcusdt@kline_1s",
    #"wss://data-stream.binance.vision/ws/btcusdt@kline_1s",
    #"wss://testnet.binance.vision/ws/btcusdt@kline_1s"
    #"wss://stream.binance.com/ws/btcusdt@kline_1s",

    def on_message(self, ws, message):
        data = json.loads(message)

        if "b" not in data or "a" not in data:
            return

        try:
            self.bids = pd.DataFrame(data["b"], columns=["price", "qty"]).astype(float)
            self.asks = pd.DataFrame(data["a"], columns=["price", "qty"]).astype(float)
        except:
            pass

    def start(self):
        t = threading.Thread(target=self._run)
        t.daemon = True
        t.start()

    def _run(self):
        ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message
        )
        ws.run_forever()
