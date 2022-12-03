import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

import sys
sys.path.insert(0, './') # Kullanılmak istenilenn modülün uzantısı
from data import get_dataset, get_dividends

# Zaman serisi verilerini içeren bir veri kümesi yükleyin
df = get_dataset("EREGL.IS", period="2y")
print(df.head())
print("*"*50,"\n")

def mevsimsel_ayrim(df, date_col, value_col):
    # verisetini hazırlama
    df = df.reset_index()
    df[date_col] = pd.to_datetime(df[date_col]).dt.date
    df = df[[date_col, value_col]]
    df = df.set_index(date_col)

    # Zaman serisinin mevsimselliğini ayrıştırın
    result = seasonal_decompose(df[value_col], model='additive', freq=len(df))
    
    return 