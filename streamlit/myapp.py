# in terminal: streamlit run myapp.py
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


#st.title('Medicine Selectivity Scores App')

st.write("""
# Medicine Selectivity Scores App
Shown are the scores per University and year!
""")

dfs_unified = pd.read_csv('/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/output/exported_data.csv')
#st.dataframe(dfs_unified)

# Sidebar
st.sidebar.header('User Input Features')

# Sidebar - University selection
selected_year = st.sidebar.multiselect('Year', reversed(dfs_unified['year'].unique()), reversed(dfs_unified['year'].unique()))

# Sidebar - University selection
selected_university = st.sidebar.selectbox('University', sorted(dfs_unified['university'].unique()))

# Filtering data
df_selected_university_year = dfs_unified[(dfs_unified['university'] == selected_university) & (dfs_unified['year'].isin(selected_year))]

st.header('Display Scores of Selected University and Year')
st.write('Data Dimension: ' + str(df_selected_university_year.shape[0]) + ' rows and ' + str(df_selected_university_year.shape[1]) + ' columns.')
st.dataframe(df_selected_university_year)



#st.line_chart(data)



#define the ticker symbol
#tickerSymbol = 'GOOGL'
#get data on this ticker
#tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
#tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

#st.line_chart(tickerDf.Close)
#st.line_chart(tickerDf.Volume)

