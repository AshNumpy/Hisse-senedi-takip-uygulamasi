import streamlit as st
from streamlit_option_menu import option_menu
from data import get_dataset
from data import get_dividends
from data import semboller

st.set_page_config(layout="wide")

d1,d2,d3,d4 = st.columns(4)

with d1:
    hisse = st.selectbox(
    "Hisse Adı",
    (semboller)
)

with d2:
    frekans = st.selectbox(
        "Frekans",
        # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        ("Günlük", "5 Günlük", "Haftalık", "3 Aylık")
    )
    
with d3: 
    st.date_input('Başlangıç Tarihi')
    
with d4:
    st.date_input('Bitiş Tarihi')


    
selected = option_menu(
        menu_title = None,
        options =["Veriler","Temel Analiz", "Grafikler", "ZS Analiz", "Makine Öğrenmesi", "Derin Öğrenme"],
        icons=["bookshelf","bar-chart", "graph-up", "clock-history", "cpu", "gpu-card"],
        orientation = "horizontal",
        default_index = 0
)

if selected == "Veriler":
    st.subheader(f'{hisse} Açılış Kapanış Hacim Verileri')
    df = get_dataset(f"{hisse}.IS")
    df = df.sort_index(ascending=False)
    st.dataframe(df, use_container_width=True)
    st.write("---")

    st.subheader('Yıllara Göre Temettü')
    df_dd = get_dividends(f"{hisse}.IS")
    
    df_dd = df_dd.sort_index(ascending=False)
    st.table(df_dd)
    
if selected == "Temel Analiz":
    st.title(f"You have selected {selected}")
    
if selected == "Grafikler":
    df = get_dataset(f"{hisse}.IS")
    st.line_chart(df['Close'])
    
if selected == "ZS Analiz":
    st.subheader(f"You have selected {selected}")
    
if selected == "Yapay Zeka":
    st.subheader(f"You have selected {selected}")




