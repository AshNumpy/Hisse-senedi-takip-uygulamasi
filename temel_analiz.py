import pandas as pd
import numpy as np 
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
    left, middle, right = st.columns(3)
    with left:
        st.subheader("Intro to Dataframe")
        st.dataframe(df)
    with middle:
        st.subheader("Dividends")
        st.dataframe(dividends)
    with right:
        st.subheader("Summary Statistics")
        st.table(df.describe())
    st.write("---")
