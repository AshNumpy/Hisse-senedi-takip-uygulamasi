import pandas as pd 
import numpy as np 
import streamlit as st

# -- Modules -- 
from data import get_dataset
from data import get_dividends

df = get_dataset("EREGL.IS")
dividends = get_dividends("EREGL.IS")

def grafikler():
    import plotly.graph_objects as go

    fig = go.Figure(data = [go.Candlestick(x=df.index,
        open = df['Open'], 
        high=df['High'],
        low = df['Low'], 
        close = df['Close']
    )])

    
    st.plotly_chart(fig)

grafikler()
