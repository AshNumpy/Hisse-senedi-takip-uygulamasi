import pandas as pd
import numpy as np

def ts_analysis(df, date_col, value_col, data_period, p, d, q, arima_model_type="multiplicative"):

    # kütüphaneler
    import matplotlib.pyplot as plt
    import pandas as pd
    from statsmodels.tsa.seasonal import seasonal_decompose
    from sklearn.linear_model import LinearRegression
    from statsmodels.tsa.arima_model import ARIMA
    
    # veri setini hazırla
    df = df.reset_index()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df[[date_col, value_col]]
    df = df.set_index(date_col)

    # Mevsimsellikleri belirle
    mevsimsellikler = seasonal_decompose(df, model=arima_model_type, period=data_period)

    # Trendleri belirle
    X = range(len(df))
    y = df[value_col].values
    model = LinearRegression()
    model.fit(X, y)

    # Trendleri göster
    trend = model.predict(X) # trend plotlanmalı 

    # Varyansları belirle
    arima = ARIMA(df, order=(p, d, q))
    arima_fit = arima.fit(disp=False)

    # Varyansları göster
    residuals = arima_fit.resid # varyanslar plotlanmalı

    # tahminler yap
    preds = arima_fit.predict()
    
    return mevsimsellikler, trend, model, residuals, preds