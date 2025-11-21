import pandas as pd
import requests

class OrderbookClient:
    def __init__(self, symbol="btcusdt"):
        self.symbol = symbol

    def get_depth_raw(self, limit=20):
        url = f"https://api.binance.com/api/v3/depth?symbol={self.symbol.upper()}&limit={limit}"
        r = requests.get(url).json()
        return r

    def get_depth(self, limit=20):
        """Return bids_df, asks_df, AND raw JSON."""
        raw = self.get_depth_raw(limit)

        bids = pd.DataFrame(raw["bids"], columns=["price", "qty"], dtype=float)
        asks = pd.DataFrame(raw["asks"], columns=["price", "qty"], dtype=float)

        return raw, bids, asks
