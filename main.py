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
    f_secenek = {"60m":"15 Dakika", "1d": "Günlük", "5d": "5 Günlük", "1wk": "Haftalık", "mo": " Aylık", "3mo": "3 Aylık"}
    def format_func(option):
        return f_secenek[option]
    frekans = st.selectbox(
        "Frekans",
        f_secenek.keys(), 
        format_func=lambda x:f_secenek[ x ],
        index =1
        
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
# with d3: 
#     st.date_input('Başlangıç Tarihi')
    
# with d4:
#     st.date_input('Bitiş Tarihi')


selected = option_menu(
        menu_title = None,
        options =["Veriler","Temel Analiz", "Grafikler", "ZS Analiz", "Makine Öğrenmesi", "Derin Öğrenme"],
        icons=["bookshelf","bar-chart", "graph-up", "clock-history", "cpu", "gpu-card"],
        orientation = "horizontal",
        default_index = 2
        
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
    df = get_dataset(f"{hisse}.IS", periyot, frekans)
    st.line_chart(df['Close'])
    
if selected == "ZS Analiz":
    st.subheader(f"You have selected {selected}")
    
if selected == "Yapay Zeka":
    st.subheader(f"You have selected {selected}")




