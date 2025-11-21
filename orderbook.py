import requests
import pandas as pd

class OrderbookClient:
    def __init__(self, symbol="BTCUSDT"):
        self.url = f"wss://data-stream.binance.vision/ws/{SYMBOL}@kline_1s"

    def get_depth(self):
        r = requests.get(self.url, timeout=5)

        try:
            raw = r.json()
        except:
            return {}, pd.DataFrame(), pd.DataFrame()

        # Jika API diblokir
        if "bids" not in raw:
            return raw, pd.DataFrame(), pd.DataFrame()

        bids = pd.DataFrame(raw["bids"], columns=["price", "qty"]).astype(float)
        asks = pd.DataFrame(raw["asks"], columns=["price", "qty"]).astype(float)

        return raw, bids, asks
