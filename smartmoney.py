
import pandas as pd
import numpy as np

def compute_smart_money(df):
    df['return'] = df['close'].pct_change()
    df['CVD'] = np.where(df['return']>0, df['volume'], -df['volume']).cumsum()
    return df
