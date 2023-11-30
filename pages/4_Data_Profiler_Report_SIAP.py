#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit as st

from streamlit_ydata_profiling import st_profile_report

df = pd.read_parquet('/Users/luiser/Desktop/MCD/Ing Caract/Proyecto_Ing_Caract-main 3/RedDelBancoDeAlimentos_Dashboard-Luiser-EDA/data/SIAP.parquet')
pr = ProfileReport(df, minimal=True, orange_mode=True, explorative=True)

st_profile_report(pr, navbar=True)


# In[ ]:




