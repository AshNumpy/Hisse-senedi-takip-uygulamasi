import pandas as pd 
import numpy as np 
import streamlit as st

# don't show info messages
import logging
logger = logging.getLogger('cmdstanpy')
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.CRITICAL)

# -- Modules --
import sys
sys.path.insert(0, './') # Kullanılmak istenilenn modülün uzantısı
from data import get_dataset, get_dividends

df = get_dataset("EREGL.IS", period="3y")

def forecasting(df, date_column, value_column, train_size=0.75, freq='D', prediction_periods=30, country_code='TR'):
    """"
    Inputs:\n
    df: dataframe\n
    date_column: Name of the Date column. If date column on the index you should write just name of that and keep moving.\n
    value_column: Price or whatever column that has the values.\n
    train_size: !! Where should function cut off the dfset as train.\n
    freq: Frequency of the df , default = Daily.\n
    \t\t'D':Daily, 'W':Weekly, 'Y':Yearly\n
    prediction_periods: How many periods you want to do forecast.\n
    country_name: Name of the country that dfs belong it. It necessary for the holidays effect, default = TR\n
    \n
    Libraries: prophet from facebook\n
    \n
    Returns:\n
    model: Forecasting model.\n
    forecast: Predicted values.\n
    training_df: Training df.\n
    test_df: Test df\n
    """

    # importing the librarie(s)
    from prophet import Prophet
    import logging
    logging.getLogger('fbprophet').setLevel(logging.WARNING)    

    # prepare the df for forecasting
    df = df.reset_index()
    df = df[[date_column, value_column]].dropna(axis=0)
    df.columns = ['ds', 'y']

    # splitting for accuracy testing
    cutoff = df.iloc[int(np.round(len(df)*train_size)),]['ds']
    train = df[df['ds'] < cutoff]
    test = df[df['ds'] > cutoff]
    
    # model building
    model = Prophet()
    model.add_country_holidays(country_name=country_code)
    model.fit(train)
    
    # set future times to do forecasting
    future = model.make_future_dataframe(periods=prediction_periods, freq=freq)
    
    # make predictions
    forecast = model.predict(future)
    print("Process is Succesfully DONE!")
    
    return model, forecast, train, test

model, forecast, train, test = forecasting(df, date_column='Date', value_column='Close')

forecast = forecast[['ds', 'yhat_lower', 'yhat_upper', 'yhat']]
forecast = forecast.sort_values(by='ds', ascending=False)

# fig = model.plot(forecast)
# fig.legend(loc='upper left', fontsize='large')
# plt.show()

# fig = model.plot_components(forecast)
# fig.tight_layout(h_pad=5)
# plt.show()


# Accuracy 
y_pred = forecast.iloc[:test.shape[0],-1]
print(forecast.shape)
print(test.shape)
print(y_pred.shape)

from sklearn.metrics import mean_absolute_percentage_error

MAPE = mean_absolute_percentage_error(y_pred, test['y'])
print(f"MAPE: {np.round(MAPE,2)*100:.2f}")