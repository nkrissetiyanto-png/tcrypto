import numpy as np
from sklearn.ensemble import RandomForestRegressor


class AIPredictor:
    def __init__(self):
        # model yang ringan & stabil di Streamlit Cloud
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            random_state=42,
        )
        self.trained = False

    def train(self, df):
        # fitur sederhana: close, volume, return
        temp = df.copy().dropna().tail(300)  # batasi supaya ringan
        temp["return"] = temp["close"].pct_change().fillna(0)

        X = temp[["close", "volume", "return"]].values
        y = temp["close"].shift(-1).fillna(method="ffill").values

        self.model.fit(X, y)
        self.trained = True

    def predict(self, df):
        if len(df) < 10:
            return float(df["close"].iloc[-1])

        if not self.trained:
            self.train(df)

        last = df.tail(2).copy()
        last["return"] = last["close"].pct_change().fillna(0)
        row = last.iloc[-1]

        X_last = np.array([[row["close"], row["volume"], row["return"]]])
        pred_price = float(self.model.predict(X_last)[0])

        return pred_price
