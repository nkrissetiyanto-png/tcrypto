
import threading
import websocket
import json
import pandas as pd

class CryptoWebSocket:
    def __init__(self, pair):
        self.url = f"wss://stream.binance.com:9443/ws/{pair}@kline_1m"
        self.last_candle = None

    def on_message(self, ws, msg):
        data = json.loads(msg)
        k = data['k']
        self.last_candle = {
            'time': pd.to_datetime(k['T'], unit='ms'),
            'open': float(k['o']),
            'high': float(k['h']),
            'low': float(k['l']),
            'close': float(k['c']),
            'volume': float(k['v'])
        }

    def start(self):
        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self):
        ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message
        )
        ws.run_forever()
