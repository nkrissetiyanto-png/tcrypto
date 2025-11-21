import numpy as np
from sklearn.ensemble import RandomForestRegressor


class AIPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=120,
            max_depth=6,
            random_state=42
        )
        self.trained = False


    def safe_last_close(self, df):
        """Return last close safely without crashing."""
        try:
            return float(df["close"].iloc[-1])
        except:
            return None


    def train(self, df):
        # Minimal data requirement: 20 bars
        if df is None or len(df) < 20:
            self.trained = False
            return

        temp = df.copy().tail(300).dropna()

        temp["return"] = temp["close"].pct_change().fillna(0)

        # Features
        X = temp[["close", "volume", "return"]].values
        y = temp["close"].shift(-1).fillna(method="ffill").values

        self.model.fit(X, y)
        self.trained = True


    def predict(self, df):
        """
        Predict next 1-minute close price with full safety.
        """

        # If no data, return None safely
        if df is None or len(df) == 0:
            return None

        # If only 1 bar, return that bar
        if len(df) < 5:
            return self.safe_last_close(df)

        # Train if not trained
        if not self.trained:
            self.train(df)

        # If still not trained, fallback
        if not self.trained:
            return self.safe_last_close(df)

        # SAFE extract last values
        last_close = float(df["close"].iloc[-1])
        last_vol = float(df["volume"].iloc[-1])
        last_return = df["close"].pct_change().iloc[-1]
        if np.isnan(last_return):
            last_return = 0

        X_last = np.array([[last_close, last_vol, last_return]])

        try:
            pred_price = float(self.model.predict(X_last)[0])
            return pred_price
        except:
            return self.safe_last_close(df)
