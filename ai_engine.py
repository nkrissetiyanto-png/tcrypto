
import numpy as np
from lightgbm import LGBMRegressor

class AIPredictor:
    def __init__(self):
        self.model = LGBMRegressor()
        self.trained = False

    def train(self, df):
        df['return'] = df['close'].pct_change().fillna(0)
        X = df[['close','volume','return']]
        y = df['close'].shift(-1).fillna(method='ffill')
        self.model.fit(X, y)
        self.trained = True

    def predict(self, df):
        if not self.trained:
            self.train(df)
        last = df.iloc[-1]
        X = np.array([[last['close'], last['volume'], df['close'].pct_change().iloc[-1]]])
        return float(self.model.predict(X)[0])
