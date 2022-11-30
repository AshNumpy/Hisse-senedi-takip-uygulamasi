##IMPORTS

import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date

st.set_page_config(layout="wide")
d1, d2,d3 = st.columns(3)
with d1:
    st.selectbox(
    "Hisse Adı",
    ('LIDER.IS', 'BRSAN.IS', 'IPEKE.IS')
)


with d2: 
    st.date_input('Başlangıç Tarihi')
with d3:
    st.date_input('Bitiş Tarihi', max_value=date.today())
    
selected = option_menu(
        menu_title = None,
        options =["Temel Analiz", "Grafikler", "ZS Analizi"],
        icons=["bar-chart", "graph-up", "clock-history"],
        orientation = "horizontal",
        default_index = 1
)

if selected == "Temel Analiz":
    st.title(f"{selected} Verileri")
if selected == "Grafikler":
    st.title(f"{selected}")
if selected == "ZS Analizi":
    st.title("Zaman Serisi Analizi")




