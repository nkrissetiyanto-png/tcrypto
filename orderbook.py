import requests
import pandas as pd

class OrderbookClient:
    def __init__(self, symbol="btcusdt"):
        self.url = f"https://api.binance.com/api/v3/depth?symbol={symbol.upper()}&limit=20"

    def get_depth(self):
        try:
            raw = requests.get(self.url, timeout=5).json()

            # Fail-safe jika data tidak lengkap
            if "bids" not in raw or "asks" not in raw:
                return raw, pd.DataFrame(), pd.DataFrame()

            bids = pd.DataFrame(raw["bids"], columns=["price", "qty"], dtype=float)
            asks = pd.DataFrame(raw["asks"], columns=["price", "qty"], dtype=float)

            return raw, bids, asks

        except Exception as e:
            print("Orderbook error:", e)
            return {}, pd.DataFrame(), pd.DataFrame()
