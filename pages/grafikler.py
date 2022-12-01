import pandas as pd 
import numpy as np 
import streamlit as st

# -- Modules -- 
from data import get_dataset
from data import get_dividends

df = get_dataset("EREGL.IS")
dividends = get_dividends("EREGL.IS")

def grafikler():
    import plotly.express as px

    fig = px.line(df, x=df.index, y="Close", title='Close Price per Date')
    st.plotly_chart(fig)
    st.write("---")

    fig = px.bar(dividends, x=dividends.index, y='Dividends', text_auto=True)
    st.plotly_chart(fig)
