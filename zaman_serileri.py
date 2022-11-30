import pandas as pd 
import numpy as np
from prophet import Prophet
import streamlit as st

# -- Moduller --
from data import get_dataset
from data import get_dividends

df = get_dataset("EREGL.IS")
divs = get_dividends("EREGL.IS")
df = df.sort_index(ascending=False)


def explore():
    st.set_page_config(layout="wide")
    st.subheader("Verilerin Keşfi")
    with st.container():
        left, right = st.columns((1,2))
        with left:
            st.dataframe(df)

        with right:
            import plotly.express as px

            column = st.selectbox("Bir grafiklendirme seç", ["Close", "Open", "Volume"])

            fig = px.line(df, x=df.index, y=column)
            # fig.add_scatter(x=df.index, y=df['Open'], mode='lines')

            st.plotly_chart(fig, use_container_width=1)
    st.write("---")

    with st.container():
        col1, col2, col3 = st.columns(3)
        st.write("""
        Hangi zaman dilimine ait metrikleri görüntülemek istiyorsunuz?
        """)
        metrik_zamani = st.radio("Metrik Seçin", ["Son 1 Yıl", "Son 1 Ay", "Son 1 Hafta"])

        with col1:
            if metrik_zamani == "Son 1 Yıl":
                st.write("xxx")
                df_yil = df.groupby("")
            st.dataframe(df.describe())
            st.metric(f"Ortalama{column}", value=np.round(df.describe().loc["mean",column],2))


explore()