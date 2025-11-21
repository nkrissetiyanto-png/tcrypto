import requests
import pandas as pd

class OrderbookClient:
    def __init__(self, symbol="btcusdt"):
        self.symbol = symbol.upper()

    def get_depth(self, limit=20):
        url = "https://api.binance.com/api/v3/depth"
        params = {"symbol": self.symbol, "limit": limit}

        try:
            headers = {"User-Agent": "Mozilla/5.0"}

            r = requests.get(url, params=params, headers=headers, timeout=5).json()

            # Jika error dari Binance → return DF kosong
            if "bids" not in r or "asks" not in r:
                print("⚠ Binance returned error:", r)
                empty = pd.DataFrame({"price": [], "qty": []})
                return empty, empty

            bids = pd.DataFrame(r['bids'], columns=['price', 'qty'], dtype=float)
            asks = pd.DataFrame(r['asks'], columns=['price', 'qty'], dtype=float)

            return bids, asks

        except Exception as e:
            print("⚠ Error fetch orderbook:", e)
            empty = pd.DataFrame({"price": [], "qty": []})
            return empty, empty
