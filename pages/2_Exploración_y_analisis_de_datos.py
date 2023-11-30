import streamlit as st
import pandas as pd
import numpy as np

st.title('Exploración y Analisis de datos')

@st.cache_data
def load_data():
    data = pd.read_parquet('./data/SIAP.parquet')
    return data

data = load_data()

if st.checkbox('Show raw data'):
    st.subheader('Tidy data')
    st.write(data)

