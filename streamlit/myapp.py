# in terminal: streamlit run /Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/streamlit/myapp.py
from importlib.machinery import DEBUG_BYTECODE_SUFFIXES
from matplotlib import scale
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
import folium as folium  # pip install folium
from streamlit_folium import folium_static # pip install streamlit-folium


# wide mode
st.set_page_config(layout="wide")

#st.title('Medicine Selectivity Scores App')

st.write("""
# Medicine Selectivity Scores App
Display Scores of Selected University and Year(s)
""")

dfs_unified_orig = pd.read_csv('/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/output/exported_data.csv')

# show only relevant columns
dfs_unified = dfs_unified_orig[['year', 'university', '1_list', 'final_grade']]

# Sidebar
#st.sidebar.header('User Input Features')

# Sidebar - University selection
#selected_year = st.sidebar.multiselect('Year', reversed(dfs_unified['year'].unique()), reversed(dfs_unified['year'].unique()))
#selected_year = st.sidebar.select_slider('Slide to select period of time', options=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'])

# Sidebar - University selection
#selected_university = st.sidebar.selectbox('University', sorted(dfs_unified['university'].unique()))

# Filtering data
#df_selected_university_year = dfs_unified[(dfs_unified['university'] == selected_university) & (dfs_unified['year'].isin(selected_year))]
#df_selected_university_year = df_selected_university_year.sort_values(by=['year'], ascending=False)

#st.write('Data Dimension: ' + str(df_selected_university_year.shape[0]) + ' rows and ' + str(df_selected_university_year.shape[1]) + ' columns.')

#st.dataframe(df_selected_university_year, 1000, 2000)

prueba = pd.read_csv('/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/output/prueba.csv')

json1 = f"/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/georef-spain-comunidad-autonoma.geojson"

ma = folium.Map(location=[40,-4], zoom_start=6, width=700, height=600, control_scale=True, tiles='CartoDB Positron',
               name='Light Map', attr='My Data attribution')

choice = ['final_grade', '1_list']
choice_selected = st.selectbox('Select  convocatory', choice)

folium.Choropleth(
    geo_data=json1,
    name='choropleth',
    data=prueba,
    columns=['acom_code',choice_selected],
    key_on='feature.properties.acom_code',
    fill_color='YlGn',
    fill_opacity=0.5,
    line_opacity=0.2,
    legend_name=choice_selected
).add_to(ma)

#folium.LayerControl().add_to(ma)

folium_static(ma, width=700, height=600)








#df_selected_university_year = df_selected_university_year.melt(id_vars=['year'], value_vars=['1_list', 'final_grade'],
        #var_name='convocatory', value_name='score')

# line chart 1_list and final_grade
'''
chart = alt.Chart(df_selected_university_year).mark_line(point=True).encode(
  x=alt.X('year:N', axis=alt.Axis(title='Year')),
  y=alt.Y('score:Q', axis=alt.Axis(title='Score'), scale=alt.Scale(domain=(min(df_selected_university_year['score']), 14))),
  color=alt.Color('convocatory:N'),
  tooltip='score'
).properties(title= str(selected_university) + ' evolution of 1_list and final_grade scores across years')
st.altair_chart(chart, use_container_width=True)
'''

# line chart final_grade
#chart = alt.Chart(df_selected_university_year).mark_line(point=True).encode(
  #x=alt.X('year:N'),
  #y=alt.Y('final_grade:Q', scale=alt.Scale(domain=(min(df_selected_university_year['final_grade']), 14))),
  #color=alt.Color('university:N'),
  #tooltip='final_grade'
#).properties(title='Evolution of final_grade scores across years').interactive()
#st.altair_chart(chart, use_container_width=True)

'''
# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_university_year[['year', '1_list', 'final_grade']].to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)
'''

