import requests
import pandas as pd

class OrderbookMEXC:
    def __init__(self, symbol="BTC_USDT"):
        # MEXC depth pakai format TANPA underscore
        self.depth_symbol = symbol.replace("_", "")
        self.url = f"https://api.mexc.com/api/v3/depth?symbol={self.depth_symbol}&limit=20"

    def get_depth(self):
        try:
            raw = requests.get(self.url, timeout=3).json()

            if "bids" not in raw:
                return raw, pd.DataFrame(), pd.DataFrame()

            bids = pd.DataFrame(raw["bids"], columns=["price","qty"]).astype(float)
            asks = pd.DataFrame(raw["asks"], columns=["price","qty"]).astype(float)

            return raw, bids, asks

        except Exception as e:
            return {"error": str(e)}, pd.DataFrame(), pd.DataFrame()
