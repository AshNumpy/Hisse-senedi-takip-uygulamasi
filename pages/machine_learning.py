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
sys.path.insert(0, './Modules') # Kullanılmak istenilenn modülün uzantısı
from data import get_dataset, get_dividends

df = get_dataset("EREGL.IS", period="3y")

def forecasting(data, date_column, value_column, train_size=0.75, freq='D', prediction_periods=30, country_code='TR'):
    """"
    Inputs:\n
    data: Dataframe\n
    date_column: Name of the Date column. If date column on the index you should write just name of that and keep moving.\n
    value_column: Price or whatever column that has the values.\n
    train_size: !! Where should function cut off the dataset as train.\n
    freq: Frequency of the data , default = Daily.\n
    \t\t'D':Daily, 'W':Weekly, 'Y':Yearly\n
    prediction_periods: How many periods you want to do forecast.\n
    country_name: Name of the country that datas belong it. It necessary for the holidays effect, default = TR\n
    \n
    Libraries: prophet from facebook\n
    \n
    Returns:\n
    model: Forecasting model.\n
    forecast: Predicted values.\n
    training_data: Training data.\n
    test_data: Test data\n
    """

    # importing the librarie(s)
    from prophet import Prophet
    import logging
    logging.getLogger('fbprophet').setLevel(logging.WARNING)    

    # prepare the data for forecasting
    data = data.reset_index()
    data = data[[date_column, value_column]].dropna(axis=0)
    data.columns = ['ds', 'y']

    # splitting for accuracy testing
    cutoff = data.iloc[int(np.round(len(data)*0.8)),]['ds']
    training_data = data[data['ds'] < cutoff]
    test_data = data[data['ds'] > cutoff]

    # model building
    model = Prophet()
    model.add_country_holidays(country_name=country_code)
    
    # fitting
    model.fit(training_data)
    
    # set future times to do forecasting
    future = model.make_future_dataframe(periods=prediction_periods, freq=freq)
    
    # make predictions
    forecast = model.predict(future)
    print("Process is Succesfully DONE!")
    
    return model, forecast, training_data, test_data


model, forecast, train, test = forecasting(data=df, date_column='Date', value_column='Close',
                                                       train_size=0.85, freq='D', prediction_periods=60, country_code='TR')

# import matplotlib.pyplot as plt
# fig = model.plot(forecast)
# fig.legend(loc='upper left', fontsize='x-large')
# plt.show()

# fig = model.plot_components(forecast)
# fig.tight_layout(h_pad=5)
# plt.show()

forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

print(forecast.head())
print(forecast.tail())
print(forecast.shape)
print(test.shape)
print(train.shape)
print(df.iloc[int(np.round(len(df)*0.8)),]['Date'])