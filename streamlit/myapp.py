# in terminal: streamlit run /Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/streamlit/myapp.py
from importlib.machinery import DEBUG_BYTECODE_SUFFIXES
from tkinter import Y
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
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup

# wide mode
st.set_page_config(layout="wide")

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2, 2))

with row1_1:
    st.title("Medicine Selectivity Scores App")
    
with row1_2:
    st.write(
        """
    ##
    Displayed are the scores of public universities in Spain to study medicine (selectivity scores).
    "1_list" is the first grade to enter the univeristy and "final_grade" the last one, therefore the lowest one.
    By sliding the slider on the left you can the different scores per year.
    
    *Please note that scores shown for 2022 are predicted scores calculated by a Machine Learning model.
    """
    )

row2_1, row2_2 = st.columns((2, 2))

with row2_1:
  selected_year = st.slider("Select year", 2010, 2022)



dfs_unified = pd.read_csv('/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/output/exported_data.csv')


# Sidebar
#st.sidebar.header('User Input Features')

# Sidebar - University selection
#selected_year = st.sidebar.multiselect('Year', reversed(dfs_unified['year'].unique()), reversed(dfs_unified['year'].unique()))
#selected_year = st.sidebar.select_slider('Slide to select period of time', options=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'])

convocatory = ['final_grade', '1_list']
with row2_2:
  convocatory_selected = st.radio('Select  convocatory', convocatory)



#df_selected_university_year = df_selected_university_year.sort_values(by=['year'], ascending=False)

#st.write('Data Dimension: ' + str(df_selected_university_year.shape[0]) + ' rows and ' + str(df_selected_university_year.shape[1]) + ' columns.')

#st.dataframe(df_selected_university_year, 1000, 2000)






# LAYING OUT THE MIDDLE SECTION OF THE APP
row2_1, row2_2 = st.columns((2, 2))

df_selected_year = dfs_unified[(dfs_unified['year'] == selected_year)]

with row2_1:

# bar chart
  if convocatory_selected == '1_list':
    chart = alt.Chart(df_selected_year).mark_bar().encode(
        y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
        x=alt.X('1_list:Q', axis=alt.Axis(title='1_list'), scale=alt.Scale(domain=(min(df_selected_year['1_list']) - 0.01, max(df_selected_year['1_list']) + 0.01))),
        #color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2')),
        tooltip=('university','1_list')
      ).properties(title= str(selected_year) + ' 1_list scores', width=200, height=600)
    st.altair_chart(chart, use_container_width=True)
  else:
    chart = alt.Chart(df_selected_year).mark_bar().encode(
        y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
        x=alt.X('final_grade:Q', scale=alt.Scale(domain=(min(df_selected_year['final_grade']) - 0.01, max(df_selected_year['final_grade']) + 0.01))),
        #color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2')),
        tooltip=('university','final_grade')
      ).properties(title= str(selected_year) + ' final_grade scores', width=200, height=600)
    st.altair_chart(chart, use_container_width=True)



with row2_2:
  prueba = pd.read_csv('/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/output/prueba.csv')
  json1 = f"/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/georef-spain-comunidad-autonoma.geojson"
  m = folium.Map(location=[37,-8], zoom_start=5, width=700, height=550, control_scale=True, tiles='CartoDB Positron',
                name='Light Map', attr='My Data attribution')

  #Add layers for Popup and Tooltips

  popup = GeoJsonPopup(
      fields=['acom_name'],
      aliases=['CCAA'], 
      localize=True,
      labels=True,
      style="background-color: yellow;",
  )

  tooltip = GeoJsonTooltip(
      fields=['acom_name'],
      aliases=['CCAA'],
      localize=True,
      sticky=False,
      labels=True,
      style="""
          background-color: #F0EFEF;
          border: 1px solid black;
          border-radius: 3px;
          box-shadow: 3px;
      """,
      max_width=700,
  )


  
  # Choropleth layer
  g = folium.Choropleth(
      geo_data = json1,
      name = 'choropleth',
      data = dfs_unified,
      columns=['acom_code', 'avg_final_grade_CCAA'],
      key_on='feature.properties.acom_code',
      fill_color='YlOrRd',
      fill_opacity=0.5,
      line_opacity=0.2,
      legend_name='avg_final_grade_CCAA',
      highlight=True
  ).add_to(m)
  


  folium.GeoJson(
      json1,
      style_function=lambda feature: {
          'fillColor': '#ffff00',
          'color': 'black',
          'weight': 0.2,
          'dashArray': '5, 5'
      },
      tooltip=tooltip,
      popup=popup).add_to(g)
      

  folium.LayerControl().add_to(m)
  folium_static(m, width=700, height=550)




# LAYING OUT THE TOP SECTION OF THE APP
row3_1, row3_2 = st.columns((2, 2))

with row3_1:
    
# University selection
  selected_university = st.selectbox('Choose an university to view the convocatory selected above across years', sorted(dfs_unified['university'].unique()))

with row3_2:
    st.write(
        """
    ##
    Choose an university to view the scores across years and the correlation heatmap
    """
    )

# LAYING OUT THE MIDDLE SECTION OF THE APP
row4_1, row4_2 = st.columns((2, 2))


def line_chart_selected_uni(uni_name_selected, convocatory):
  #create y_axis name
  if convocatory == 'final_grade':
      y_axis = 'final_grade:Q'
  else:
      y_axis = '1_list:Q'
  # filter by university
  df_selected_university = dfs_unified[(dfs_unified['university'] == uni_name_selected)]
  # chart
  chart = alt.Chart(df_selected_university).mark_line(point=True).encode(
      x=alt.X('year:N', axis=alt.Axis(title='Year')),
      y=alt.Y(y_axis, axis=alt.Axis(title=convocatory), scale=alt.Scale(domain=(min(df_selected_university[convocatory]) - 0.01, max(df_selected_university[convocatory]) + 0.01))),
      tooltip=convocatory).properties(title= str(uni_name_selected) + ' evolution of ' + str(convocatory) + ' scores across years')
  return st.altair_chart(chart, use_container_width=True)




with row4_1:

  #df_selected_university_year = dfs_unified[(dfs_unified['university'] == selected_university) & (dfs_unified['year'] == selected_year)]
  #df_selected_university_year = df_selected_university_year.melt(id_vars=['year'], value_vars=['1_list', 'final_grade'],
          #var_name='convocatory', value_name='score')


  # line chart 1_list and final_grade
  line_chart_selected_uni(selected_university, convocatory_selected)
 


# line chart final_grade
#chart = alt.Chart(df_selected_university_year).mark_line(point=True).encode(
  #x=alt.X('year:N'),
  #y=alt.Y('final_grade:Q', scale=alt.Scale(domain=(min(df_selected_university_year['final_grade']), 14))),
  #color=alt.Color('university:N'),
  #tooltip='final_grade'
#).properties(title='Evolution of final_grade scores across years').interactive()
#st.altair_chart(chart, use_container_width=True)


with row4_2:
  st.set_option('deprecation.showPyplotGlobalUse', False)
  df_selected_university = dfs_unified[(dfs_unified['university'] == selected_university)]

  if convocatory_selected == '1_list':
    df = df_selected_university[['year', '1_list']]
    plt.figure(figsize=(16, 4))
    heatmap = sns.heatmap(df.corr(), vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':14}, pad=12);
    st.pyplot()
  else:
    df = df_selected_university[['year', 'final_grade']]
    plt.figure(figsize=(16, 4))
    heatmap = sns.heatmap(df.corr(), vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':14}, pad=12);
    st.pyplot()



#fig, ax = plt.subplots()
#ax.scatter([1, 2, 3], [1, 2, 3])
#other plotting actions ...
#st.pyplot(fig)

# LAYING OUT THE BOTTOM SECTION OF THE APP
row5_1, row5_2 = st.columns((2, 2))

# diff between 1_list and final_grade column

with row5_1:
  
  # bar chart
  
  chart = alt.Chart(df_selected_year).mark_bar().encode(
      y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
      x=alt.X('diff_1_list_final_grade:Q', axis=alt.Axis(title='Difference 1_list and final_grade'), scale=alt.Scale(domain=(min(df_selected_year['diff_1_list_final_grade']), max(df_selected_year['diff_1_list_final_grade'])))),
      tooltip=('university','diff_1_list_final_grade'),
      color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2'))
    ).properties(title = 'Difference between 1_list scores and final_grade for year ' + str(selected_year), width=200, height=600)
  st.altair_chart(chart, use_container_width=True)


with row5_2:
  # DO THIS WITH THE FUNCTION ABOVE; NEED TO GENERALIZE IT
  if convocatory_selected == 'final_grade':
      y_axis = 'growth_final_grade:Q'
  else:
      y_axis = 'growth_1_list:Q'
  # filter by university
  df_selected_university = dfs_unified[(dfs_unified['university'] == selected_university)]
  # chart
  chart = alt.Chart(df_selected_university).mark_line(point=True).encode(
      x=alt.X('year:N', axis=alt.Axis(title='Year')),
      y=alt.Y(y_axis, axis=alt.Axis(title= str(convocatory_selected) + ' percentage difference'), scale=alt.Scale(domain=(min(df_selected_university['growth_' + convocatory_selected]) - 0.01, max(df_selected_university['growth_' + convocatory_selected]) + 0.01))),
      tooltip=y_axis).properties(title = str(convocatory_selected)  + ' percentage difference across years')
  st.altair_chart(chart, use_container_width=True)

# IDEAS: filter by CCAA, choose zoom on map, section below only for 2022 scores, input score and tells you where you will get in, in 1_list or final_grade

row6_1, row6_2 = st.columns((2, 2))


with row6_1:
  chart = alt.Chart(dfs_unified).mark_point().encode(
      x=alt.X('growth_1_list:Q', scale = alt.Scale(domain=(min(dfs_unified['growth_1_list']) - 0.01, max(dfs_unified['growth_1_list'] + 0.01)))),
      y=alt.Y('growth_final_grade:Q', scale = alt.Scale(domain=(min(dfs_unified['growth_final_grade']) - 0.01, max(dfs_unified['growth_final_grade'] + 0.01)))), 
      color=alt.Color('university:O', scale=alt.Scale(scheme='dark2'))
  ) 
  st.altair_chart(chart, use_container_width=True)



with row6_2:
  chart = alt.Chart(df_selected_year).mark_point().encode(
      x=alt.X('diff_1_list_final_grade:Q'),
      y=alt.Y('university:O'),
      color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2'))
  )
      
  st.altair_chart(chart, use_container_width=True)
