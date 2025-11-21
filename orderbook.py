import requests
import pandas as pd

class OrderbookClient:
    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol.lower()
        self.url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=20"

    def get_depth(self):
        try:
            response = requests.get(self.url, timeout=5)

            # kalau responsenya soft-block dari Binance
            if response.status_code != 200:
                return {"error": "Binance blocked this region"}, pd.DataFrame(), pd.DataFrame()

            raw = response.json()

            if "bids" not in raw:
                return raw, pd.DataFrame(), pd.DataFrame()

            # parsing bids & asks
            bids = pd.DataFrame(raw["bids"], columns=["price", "qty"], dtype=float)
            asks = pd.DataFrame(raw["asks"], columns=["price", "qty"], dtype=float)

            return raw, bids, asks

        except Exception as e:
            return {"error": str(e)}, pd.DataFrame(), pd.DataFrame()
