import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.title('Red del Banco de Alimentos')

@st.cache_data
def load_data(x):
    if x == 'SIAP':
        data = pd.read_parquet('./data/SIAP.parquet')
    elif x == 'SNIIM':
        data = pd.read_parquet('./data/SNIIM.parquet')
    return data



#----------------------------------- SIAP --------------------------------------------------
#-------------------------------------------------------------------------------------------
df_siap = load_data('SIAP')





#----------------------------------- SNIIM --------------------------------------------------
#-------------------------------------------------------------------------------------------
df_sniim = load_data('SNIIM')
