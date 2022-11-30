import pandas as pd
import numpy as np 
import yfinance 
import streamlit as st

# -- modules -- 
from data import get_dataset
from data import get_dividends

# -- page config -- 
st.set_page_config(page_title="Hisse Takipcisi", page_icon=':bar_charts:', layout='wide')

# -- get datasets --
dividends = get_dividends(item="EREGL.IS")
df = get_dataset(item="EREGL.IS")

with st.container():
    left_side, right_side = st.columns(2)
    with left_side:
        st.subheader("Intro to Dataframe")
        st.dataframe(df)
    with right_side:
        st.subheader("Dividends")
        st.dataframe(dividends)
    st.write("---")
    