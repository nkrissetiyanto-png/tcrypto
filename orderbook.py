
import requests
import pandas as pd

class OrderbookClient:
    def __init__(self, symbol="btcusdt"):
        self.symbol = symbol.upper()

    def get_depth(self, limit=20):
        url = "https://api.binance.com/api/v3/depth"
        params = {"symbol": self.symbol, "limit": limit}
        r = requests.get(url, params=params).json()
        bids = pd.DataFrame(r['bids'], columns=['price','qty'], dtype=float)
        asks = pd.DataFrame(r['asks'], columns=['price','qty'], dtype=float)
        return bids, asks
