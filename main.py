import streamlit as st
from streamlit_option_menu import option_menu
from data import get_dataset
from data import get_dividends
from data import semboller
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

st.set_page_config(layout="wide")

d1,d2,d3,d4 = st.columns(4)

with d1:
    hisse = st.selectbox(
    "Hisse Adı",
    (semboller)
)

with d2:
    f_secenek = {"60m":"15 Dakika", "1d": "Günlük", "5d": "5 Günlük", "1wk": "Haftalık", "mo": " Aylık", "3mo": "3 Aylık"}
    def format_func(option):
        return f_secenek[option]
    frekans = st.selectbox(
        "Frekans",
        f_secenek.keys(), 
        format_func=lambda x:f_secenek[ x ],
        index = 1
        
    )
        
with d3:
    p_secenek = {"5d": "5 Günlük", "1mo": "1 Aylık", "3mo": "3 Aylık", "6mo": "6 Aylık", "1y": "1 Yıllık", "2y":"2 Yıllık", "5y": "5 Yıllık", "10y": "10 Yıllık", "ytd": "Yılbaşından bu güne", "max": "Max"}

    def format_func(option):
        return p_secenek[option]

    periyot = st.selectbox(
        "Periyot",
        p_secenek.keys(), 
        format_func=lambda x:p_secenek[ x ],
        index = 5,
        help = "Günlük veriler ile çalışılacaksa önerilen periyot Süresi 2 Yıldır"
)
    
# DATAFRAME
df = get_dataset(f"{hisse}.IS", period=periyot, interval=frekans)
dividends = get_dividends(f"{hisse}.IS")

selected = option_menu(
        menu_title = None,
        options =["Veriler","Temel Analiz", "Grafikler", "ZS Analiz", "Makine Öğrenmesi", "Derin Öğrenme"],
        icons=["bookshelf","bar-chart", "graph-up", "clock-history", "cpu", "gpu-card"],
        orientation = "horizontal",
        default_index = 0
)

if selected == "Veriler":
    st.write("---")
    st.subheader(f'{hisse} Açılış Kapanış Hacim Verileri')
    df = df.sort_index(ascending=False)
    st.dataframe(df, use_container_width=True)
    st.write("---")

    st.subheader('Yıllara Göre Temettü')
    df_dd = get_dividends(f"{hisse}.IS")
    
    df_dd = df_dd.sort_index(ascending=False)
    st.table(df_dd)
    
elif selected == "Temel Analiz":
    st.write("---")
    st.title(f"You have selected {selected}")
    
elif selected == "Grafikler":
    st.write("---")
    import sys
    sys.path.append('./Modules')
    
    from graphs import bar_chart, line_chart
    
    line = line_chart(df=df, date_col='Date', value_col='Close')
    bar = bar_chart(dividends=dividends, date='Date', values='Dividends')
    
    st.plotly_chart(line, use_container_width=True)
    st.plotly_chart(bar, use_container_width=True)
    
elif selected == "ZS Analiz":
    st.write("---")
    import sys
    sys.path.append('./Modules')
    
    from ts_analysis import ts_analysis
    
elif selected == "Yapay Zeka":
    st.write("---")
    st.subheader(f"You have selected {selected}")

elif selected == "Makine Öğrenmesi":
    st.write("---")
    secenek_col1, secenek_col2 = st.columns(2)
    with secenek_col1:
        gelecek = st.number_input('Kaç Günlük Tahminde Bulunalım?', min_value=7, value=30)
    
    with secenek_col2:
        f_secenek2 = {"d": "Günlük", "w": "Haftalık", "m": "Aylık", "y": "Yıllık"}
        def format_func(option):
            return f_secenek2[option]
        frekans2 = st.selectbox(
            "Frekans",
            f_secenek2.keys(), 
            format_func=lambda x:f_secenek2[ x ],
            index = 0)
    
    with st.spinner('Makine Öğrenimi ve Tahmin Süreci Sürüyor...'):
        import sys
        sys.path.append('./Modules')
        
        from ML import get_accuracy, do_fitting
        from graphs import bar_chart, line_chart
        
        acc_model, acc_forecast, MAE, RMSE, MAPE = get_accuracy(df=df, date_column='Date', value_column='Close', freq=frekans2)
        model, forecast = do_fitting(df=df, date_column='Date', value_column='Close', prediction_periods=gelecek, freq=frekans2)
    st.success('Tamamlandı!')
    
    st.subheader("Model Başarı Testi Sonuçları")
    
    col1, col2 = st.columns((2,1))
    with col1:
        ml_fig = model.plot(forecast)
        ml_fig.set_size_inches(16,9)
        ml_fig.legend(loc='upper left', fontsize='x-large')     
        st.pyplot(ml_fig, use_container_width=True)

    with col2:
        st.subheader("Tahmin Değerlerinin Doğruluk & Hata Metrikleri")
        MAE = np.round(MAE,2)
        st.metric("Ortalama Mutlak Hata (₺)", MAE, delta_color="inverse")

        st.metric("Hata Kareler Ortalaması Karekökü (₺)", np.round(RMSE,2))
        
        st.metric("Ortalama Yüzde Hata", np.round(MAPE,4), f"{np.round(-MAPE*100,2)}")
        
        st.metric("Modelin Tahmin Başarısı", 1-(np.round(MAPE,4)), (np.round((1-MAPE)*100,4)))
    st.write("---")
    
    st.subheader("Asıl Geleceğe Dair Tahminlere İlişkin Metrikler ve Sonuçlar")
    
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast.columns = ['Tarih', 'Tahmin Edilen Fiyatı', 'Alt Sınır', 'Üst Sınır']
    forecast.set_index("Tarih", inplace=True)
    forecast = forecast.sort_index(ascending=False)
    st.dataframe(forecast, use_container_width=True)
    
    
