import pandas as pd 
import numpy as np 
import plotly.express as px

def line_chart(df, date_col, value_col):
    df = df.reset_index()
    fig = px.line(df, x=date_col, y=value_col, title=f"{value_col} per {date_col}")
    return fig 

def bar_chart(dividends, date, values, fill_text=True):
    fig = px.bar(dividends, x=dividends.index, y='Dividends', text_auto=fill_text, title=f"{values} per {date}")
    return fig