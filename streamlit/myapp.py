import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.write("""
# Medicine Selectivity Scores App
Shown are the final scores per University and year!
""")

dfs_unified = pd.read_csv('../output/exported_data.csv')

#define the ticker symbol
#tickerSymbol = 'GOOGL'
#get data on this ticker
#tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
#tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

#st.line_chart(tickerDf.Close)
#st.line_chart(tickerDf.Volume)

