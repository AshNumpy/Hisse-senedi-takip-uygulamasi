import pandas as pd 
import numpy as np 
import streamlit as st

# -- Modules --
import sys
sys.path.insert(0, '../') # Kullanılmak istenilenn modülün uzantısı
from data import get_dataset, get_dividends

def forecasting(df, date_column, value_column, train_size=0.85, freq='d', prediction_periods=365, country_code='TR'):
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


def machine_learning(item='EREGL.IS', period="1y", train_size=.85, country_code='TR'):
    import matplotlib.pyplot as plt
    import mpld3
    import streamlit.components.v1 as components
    
    st.set_page_config(layout="wide")
    
    df = get_dataset(item, period=period)
    
    model, forecast, train, test = forecasting(df, date_column='Date', value_column='Close',
                                               prediction_periods=60, train_size=train_size, country_code=country_code)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Tahmin Sonuçları Grafiği')
            
            fig = model.plot(forecast)
            fig.set_size_inches(16,9)
            fig.legend(loc='upper left', fontsize='large')
            st.pyplot(fig)
            
        with col2:
            st.subheader("Component Grafikleri")
            
            fig = model.plot_components(forecast)
            fig.set_size_inches((13,9))
            fig.tight_layout(h_pad=5)
            
            st.pyplot(fig)
        
        forecast = forecast[['ds','yhat_lower', 'yhat_upper', 'yhat']]
        forecast = forecast.sort_values(by='ds', ascending=False)
        
        st.write("---")
    
    with st.container():
        col1 , col2 = st.columns(2)
        
        with col1:
            st.subheader("Tahmin Sonuçları")
            st.dataframe(forecast, use_container_width=1)
            
        with col2:
            test = test.sort_index(ascending=False)

            y_pred = forecast[forecast['ds'].isin(test['ds'])][['ds', 'yhat']]
    
            from sklearn.metrics import mean_absolute_percentage_error
            MAPE = mean_absolute_percentage_error(y_pred['yhat'] , test['y'])

            st.markdown("<h3 style='text-align: center; color: lightblue;'>Tahmin Sonuçlarının Metrikleri</h3>", unsafe_allow_html=True)
            
            st.metric("MAPE",
                  value=f"{np.round(MAPE,2)*100:.2f}%", delta=f"{np.round(-MAPE,4)*100:.2f}%")
                
            st.metric("Accuracy Rate",
                    value=f"{np.round(1- MAPE,2)*100:.2f}%", delta=f"{np.round(1 - MAPE,4)*100:.2f}%")


machine_learning()