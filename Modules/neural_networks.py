import pandas as pd

import sys
sys.path.insert(0, './')
from data import get_dataset

def get_df_with_numeric_date(item, period="max", future=30):
    try:
        df = get_dataset(item, period=period)
    except:
        print("Hisse senedi item adını yanlış girdiniz sonuna '.IS' girdiğinden emin olunuz . Örneğin 'EREGL.IS' ")
    
    df = df.reset_index()
    df = df.dropna()
    df = df[df["Close"] >= 0]
    df = df.sort_values(by="Date")
            
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Date_num"] = df["Date"].apply(lambda x: x.timestamp())
    
    # gelecek tarihleri oluşturalım    
    son_tarih = df['Date'].max()
    gelecek_tarih = son_tarih + pd.Timedelta(days=future)

    tarihler = pd.date_range(start=son_tarih, end=gelecek_tarih)
    tarihler_df = pd.DataFrame({"Date": tarihler})
    tarihler_df['Date'] = pd.to_datetime(tarihler_df["Date"], format="%Y-%m-%d")
    tarihler_df["Date_num"] = tarihler_df["Date"].apply(lambda x: x.timestamp())

    return df, tarihler_df


