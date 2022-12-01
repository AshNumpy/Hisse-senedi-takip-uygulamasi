##IMPORTS

import streamlit as st
from streamlit_option_menu import option_menu
from sembol_listesi import semboller

st.set_page_config(layout="wide")
d1, d2,d3 = st.columns(3)
with d1:
    st.selectbox(
    "Hisse Adı",
    (semboller)
)

with d2: 
    st.date_input('Başlangıç Tarihi')
with d3:
    st.date_input('Bitiş Tarihi')
    
selected = option_menu(
        menu_title = None,
        options =["Veriler","Temel Analiz", "Grafikler", "ZS Analiz", "Makine Öğrenmesi"],
        icons=["bookshelf","bar-chart", "graph-up", "clock-history", "cpu"],
        orientation = "horizontal",
        default_index = 1
)
if selected == "Veriler":
    st.title(f"You have selected {selected}")
if selected == "Temel Analiz":
    st.title(f"You have selected {selected}")
if selected == "Grafikler":
    st.title(f"You have selected {selected}")
if selected == "ZS Analiz":
    st.title(f"You have selected {selected}")
if selected == "Yapay Zeka":
    st.title(f"You have selected {selected}")




