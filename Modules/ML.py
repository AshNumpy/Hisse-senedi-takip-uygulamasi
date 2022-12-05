import pandas as pd 
import numpy as np 

def get_accuracy(df, date_column, value_column, train_size=0.85, freq='d', prediction_periods=365, country_code='TR'):
    """"
    Inputs:\n
    df: dataframe\n
    date_column: Name of the Date column. If date column on the index you should write just name of that and keep moving.\n
    value_column: Price or whatever column that has the values.\n
    train_size: !! Where should function cut off the df as train.\n
    freq: Frequency of the df , default = Daily.\n
    \t\t'D':Daily, 'W':Weekly, 'Y':Yearly\n
    prediction_periods: How many periods you want to do forecast.\n
    country_name: Name of the country that dfs belong it. It necessary for the holidays effect, default = TR\n
    \n
    Libraries:\n
    ~ prophet\n
    ~ sklearn
    \n
    Returns:\n
    model: Forecasting model.\n
    forecast: Predicted values.\n
    train: Training dataframe.\n
    test: Test dataframe\n
    MAE: Mean Absolute Error\n
    RMSE: Root Mean Squared Error\n
    MAPE: Mean Absolute Percentage Error
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
    print("Accuracy Process is Succesfully DONE!")
    
    # calculate accuracy
    y_pred = forecast[forecast['ds'].isin(test['ds'])]['yhat']

    from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
    
    MAE = mean_absolute_error(test['y'], y_pred)
    RMSE = np.sqrt(mean_squared_error(test['y'], y_pred))
    MAPE = mean_absolute_percentage_error(test['y'], y_pred)


    return model, forecast, MAE, RMSE, MAPE


def do_fitting(df, date_column, value_column, freq='d', prediction_periods=42, country_code='TR'):
    
    # importing the librarie(s)
    from prophet import Prophet
    import logging
    logging.getLogger('fbprophet').setLevel(logging.WARNING)

    # prepare the df for forecasting
    df = df.reset_index()
    df = df[[date_column, value_column]].dropna(axis=0)
    df.columns = ['ds', 'y']
    
    # model building
    model = Prophet()
    model.add_country_holidays(country_name=country_code)
    model.fit(df)
    
    # set future times to do forecasting
    future = model.make_future_dataframe(periods=prediction_periods, freq=freq)
    
    # make predictions
    forecast = model.predict(future)
    print("Process is Succesfully DONE!")
    
    return model, forecast