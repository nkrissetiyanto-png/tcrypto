import requests
import pandas as pd

class OrderbookMEXC:
    def __init__(self, symbol="BTC_USDT"):
        self.symbol = symbol

    def get_depth(self):
        url = f"https://api.mexc.com/api/v3/depth?symbol={self.symbol}&limit=20"
        r = requests.get(url, timeout=5).json()

        if "bids" not in r or "asks" not in r:
            return r, pd.DataFrame(), pd.DataFrame()

        bids = pd.DataFrame(r["bids"], columns=["price","qty"]).astype(float)
        asks = pd.DataFrame(r["asks"], columns=["price","qty"]).astype(float)

        return r, bids, asks
