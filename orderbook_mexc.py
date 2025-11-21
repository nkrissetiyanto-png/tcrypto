import requests
import pandas as pd

class OrderbookMEXC:
    def __init__(self, symbol="BTC_USDT"):
        self.symbol = symbol

    def get_depth(self):
        url = f"https://api.mexc.com/api/v3/depth?symbol={self.symbol}&limit=20"
        r = requests.get(url)

        raw = r.json()

        if "bids" not in raw or "asks" not in raw:
            return raw, pd.DataFrame(), pd.DataFrame()

        bids = pd.DataFrame(raw["bids"], columns=["price","qty"]).astype(float)
        asks = pd.DataFrame(raw["asks"], columns=["price","qty"]).astype(float)

        return raw, bids, asks
