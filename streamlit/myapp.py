# in terminal: streamlit run /Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/streamlit/myapp.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
import folium as folium  # pip install folium
from streamlit_folium import folium_static # pip install streamlit-folium
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
import geopandas as gpd
from folium.plugins import MarkerCluster

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
    "1_list" is the first grade to enter the university and "final_grade" the last one, therefore the lowest one.
    By sliding the slider on the left you can the different scores per year.
    
    *Please note that scores shown for 2022 are predicted scores calculated by a Machine Learning model.
    """
    )

row2_1, row2_2, row2_3, row2_4 = st.columns((3, 1, 1, 1))

with row2_1:
  year_selected = st.slider("Select year", 2010, 2022)



dfs_unified = pd.read_csv('/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/output/exported_data.csv')


convocatory = ['final_grade', '1_list']
df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected)]


CCAA = list(df_year_selected['CCAA'].unique())
CCAA.append('All')



with row2_2:
  CCAA_selected = st.selectbox('Filter by CCAA (optional)', sorted(CCAA))

with row2_4:
  convocatory_selected = st.radio('Select  convocatory', convocatory)

with row2_3:
  score_introduced = st.text_input('Filter by score (optional) (e.g., 12.5)')

  if (score_introduced == ''):
    pass
  else:
    try:
      float(score_introduced)
    except ValueError:
      st.error('Please enter a number')
  
  # falta manejo de errores, de 0-14, da error cuando filtras por CCAA y pones un numero menor que el minimo, etc.

 
#df_selected_university_year = df_selected_university_year.sort_values(by=['year'], ascending=False)

#st.write('Data Dimension: ' + str(df_selected_university_year.shape[0]) + ' rows and ' + str(df_selected_university_year.shape[1]) + ' columns.')

#st.dataframe(df_selected_university_year, 1000, 2000)




# LAYING OUT THE MIDDLE SECTION OF THE APP
row2_1, row2_2 = st.columns((2, 2))


if (CCAA_selected == 'All') & (score_introduced == ''):
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected)]
elif (CCAA_selected != 'All') & (score_introduced == ''):
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified['CCAA'] == CCAA_selected)]
elif (CCAA_selected == 'All') & (score_introduced != ''):
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified[convocatory_selected] <= float(score_introduced))]
else:
  #(CCAA_selected != 'All') & (score_introduced != '')
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified['CCAA'] == CCAA_selected) & (dfs_unified[convocatory_selected] <= float(score_introduced))]

with row2_1:
# # test
#   if convocatory_selected == 'final_grade':
#       bars = alt.Chart(df_year_selected).mark_bar().encode(
#           x='final_grade:Q',
#           y='university:O'
#         )
#       text = bars.mark_text(
#         align='left',
#         baseline='middle',
#         color='white',
#         dx=3  # Nudges text to right so it doesn't appear on top of the bar
#       ).encode(
#         text='final_grade:Q'
#       )

#       graph = (bars + text).properties(width = 200, height=600)
#       st.altair_chart(graph, use_container_width=True)
#   else:
#     print('hola')

# bar chart
  if convocatory_selected == '1_list':
    chart = alt.Chart(df_year_selected).mark_bar().encode(
        x=alt.X('1_list:Q', axis=alt.Axis(title='1_list'), scale=alt.Scale(domain=(min(df_year_selected['1_list']) - 0.05, max(df_year_selected['1_list']) + 0.05))),
        y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
        #color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2')),
        tooltip=('university','1_list')
      )
    
    text = chart.mark_text(
      align='left',
      baseline='middle',
      color='white',
      dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
      text='1_list:Q'
    )

    graph = (chart + text).properties(title= str(year_selected) + ' 1_list scores', width=200, height=600)
    
    st.altair_chart(graph, use_container_width=True)

  else:
    chart = alt.Chart(df_year_selected).mark_bar().encode(
        x=alt.X('final_grade:Q', scale=alt.Scale(domain=(min(df_year_selected['final_grade']) - 0.05, max(df_year_selected['final_grade']) + 0.05))),
        y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
        #color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2')),
        tooltip=('university','final_grade')
      )

    text = chart.mark_text(
      align='left',
      baseline='middle',
      color='white',
      dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
      text='final_grade:Q'
    )
    
    graph = (chart + text).properties(title= str(year_selected) + ' final_grade scores', width=200, height=600)
  
    st.altair_chart(graph, use_container_width=True)




# map
def create_marker(map, latitude, longitude, popup_info, tooltip_info, color_marked):
   folium.Marker(
      location=[latitude, longitude], # coordinates for the marker (Earth Lab at CU Boulder)
      popup=popup_info, # pop-up label for the marker,
      tooltip=tooltip_info , # tooltip label for the marker
      icon=folium.Icon(color=color_marked)).add_to(map)


  # #prueba = pd.read_csv('/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/output/prueba.csv')
  # f = folium.Figure(width=700, height=550)
  # json1 = f"/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/georef-spain-comunidad-autonoma.geojson"
  # m = folium.Map(location=[37,-8], zoom_start=5, width=700, height=550, control_scale=True, tiles='CartoDB Positron',
  #               name='Light Map', attr='My Data attribution').add_to(f)

  # #Add layers for Popup and Tooltips

  # popup = GeoJsonPopup(
  #     fields=['acom_name'],
  #     aliases=['CCAA'], 
  #     localize=True,
  #     labels=True,
  #     style="background-color: yellow;",
  # )

  # tooltip = GeoJsonTooltip(
  #     fields=['acom_name'],
  #     aliases=['CCAA'],
  #     localize=True,
  #     sticky=False,
  #     labels=True,
  #     style="""
  #         background-color: #F0EFEF;
  #         border: 1px solid black;
  #         border-radius: 3px;
  #         box-shadow: 3px;
  #     """,
  #     max_width=700,
  # )
  


  # # Choropleth layer
  # g = folium.Choropleth(
  #     geo_data = json1,
  #     name = 'choropleth',
  #     data = df_year_selected,
  #     columns=['acom_code', 'avg_final_grade_CCAA'],
  #     key_on='feature.properties.acom_code',
  #     fill_color='YlOrRd',
  #     fill_opacity=0.5,
  #     line_opacity=0.2,
  #     legend_name='avg_final_grade_CCAA',
  #     highlight=True
  # ).add_to(m)
  

  # folium.GeoJson(
  #     json1,
  #     style_function=lambda feature: {
  #         'fillColor': '#ffff00',
  #         'color': 'black',
  #         'weight': 0.2,
  #         'dashArray': '5, 5'
  #     },
  #     tooltip=tooltip,
  #     popup=popup).add_to(g)

  
  # #folium.LayerControl().add_to(m)
  # folium_static(f, width=700, height=550)

with row2_2:

  f = folium.Figure(width=800, height=550)

# change latitude, longitude and zoom of map based on CCAA selected
  if CCAA_selected == 'All':
    latitude_map = 40.4167047
    longitude_map = -3.7035825
    zoom_map = 6
  elif CCAA_selected == 'Comunidad de Madrid':
    latitude_map = 40.4167047
    longitude_map = -3.7035825
    zoom_map = 10
  elif CCAA_selected == 'Cataluña':
    latitude_map = 41.37921475
    longitude_map = 2.17941527
    zoom_map = 8
  elif CCAA_selected == 'Aragón':
    latitude_map = 41.6421312
    longitude_map = -0.90302271
    zoom_map = 8
  elif CCAA_selected == 'Castilla y León':
    latitude_map = 41.4105937
    longitude_map = -5.0916619
    zoom_map = 8
  elif CCAA_selected == 'Cantabria':
    latitude_map = 43.4736983
    longitude_map = -3.7859174
    zoom_map = 8
  elif CCAA_selected == 'Galicia':
    latitude_map = 42.88050025
    longitude_map = -8.5457602
    zoom_map = 8
  elif CCAA_selected == 'Extremadura':
    latitude_map = 38.8824069
    longitude_map = -7.0194457
    zoom_map = 8
  elif CCAA_selected == 'Andalucía':
    latitude_map = 37.4128557
    longitude_map = -3.7845606
    zoom_map = 7
  elif CCAA_selected == 'Castilla-La Mancha':
    latitude_map = 38.4527362
    longitude_map = -3.05363374
    zoom_map = 8
  elif CCAA_selected == 'País Vasco':
    latitude_map = 43.3359821
    longitude_map = -2.9768285
    zoom_map = 8
  elif CCAA_selected == 'Canarias':
    latitude_map = 28.09055808
    longitude_map = -15.41890014
    zoom_map = 7
  elif CCAA_selected == 'Comunitat Valenciana':
    latitude_map = 39.4786642
    longitude_map = -0.3627246
    zoom_map = 8
  elif CCAA_selected == 'Principado de Asturias':
    latitude_map = 43.3533657
    longitude_map = -5.8687712
    zoom_map = 8
  elif CCAA_selected == 'Illes Balears':
    latitude_map = 39.60701435
    longitude_map = 2.64475448
    zoom_map = 8
  elif CCAA_selected == 'Comunidad Foral de Navarra':
    latitude_map = 42.8154264
    longitude_map = -1.65263107
    zoom_map = 8
  else:
    latitude_map = 40.4167047
    longitude_map = -3.7035825
    zoom_map = 6

  m = folium.Map(location=[latitude_map, longitude_map], zoom_start=zoom_map, width=800, height=550, control_scale=True, tiles='CartoDB Positron',
                  name='Light Map', attr='My Data attribution').add_to(f)

  
# sortby y hacer un head o tail, y en funcion de eso, poner un color u otro y luego crear una leyenda con los colores
  
# ojo en 2010 hay menos unis

  list_unis_year_selected = list(df_year_selected['university'].unique())
  # iterate through list
  #list_unis_year_selected = ['u. autónoma de barcelona']
  
  for uni in list_unis_year_selected:
    latitude_uni = df_year_selected.loc[df_year_selected['university'] == uni, 'latitude'].mean()
    longitude_uni = df_year_selected.loc[df_year_selected['university'] == uni, 'longitude'].mean()
    
    if convocatory_selected == '1_list':
      score = df_year_selected.loc[df_year_selected['university'] == uni, '1_list'].mean()
    else:
      score = df_year_selected.loc[df_year_selected['university'] == uni, 'final_grade'].mean()
     
    if score < 12.5:
      color_marked = 'blue'
    elif 12.5 <= score < 13.3:
      color_marked = 'gray'
    else:
      color_marked = 'red'

    
    #print(latitude_uni, longitude_uni, score, uni, color_marked)
    create_marker(m, latitude_uni, longitude_uni, convocatory_selected + ': ' + str(score), uni + ': ' + str(score), color_marked)
    
  #create_marker(m, 41.502593, 2.080056, 'u. autónoma de barcelona', 13.0, 'darkred')
  # Display the map
  folium_static(f, width=800, height=550)



# scores by CCAA
df_CCAA_year_selected = df_year_selected.groupby('CCAA')[convocatory_selected].mean().reset_index()
# round to 3 decimals
df_CCAA_year_selected[convocatory_selected] = df_CCAA_year_selected[convocatory_selected].apply(lambda x: round(x, 3))

# bar chart
if convocatory_selected == '1_list':
  chart = alt.Chart(df_CCAA_year_selected).mark_bar().encode(
      x=alt.X('CCAA:O', sort='-y', axis=alt.Axis(title='CCAA', labelAngle=-0)),
      y=alt.Y('1_list:Q', axis=alt.Axis(title='1_list'), scale=alt.Scale(domain=(min(df_CCAA_year_selected['1_list']) - 0.05, max(df_CCAA_year_selected['1_list']) + 0.05))),
      #color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2')),
      tooltip=('CCAA','1_list')
    )

  text = chart.mark_text(
      align='center',
      baseline='bottom',
      color='white',
      dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
      text='1_list:Q'
    )
    
  graph = (chart + text).properties(title= str(year_selected) + ' average 1_list scores by CCAA', width = 200, height = 400)
  
  st.altair_chart(graph, use_container_width=True)

else:
  chart = alt.Chart(df_CCAA_year_selected).mark_bar().encode(
      x=alt.X('CCAA:O', sort='-y', axis=alt.Axis(title='CCAA', labelAngle=-0)),
      y=alt.Y('final_grade:Q', scale=alt.Scale(domain=(min(df_CCAA_year_selected['final_grade']) - 0.05, max(df_CCAA_year_selected['final_grade']) + 0.05))),
      #color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2')),
      tooltip=('CCAA','final_grade')
    )
  
  text = chart.mark_text(
      align='center',
      baseline='bottom',
      color='white',
      dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
      text='final_grade:Q'
    )
    
  graph = (chart + text).properties(title= str(year_selected) + ' average final_grade scores by CCAA', width = 200, height = 400)
  
  st.altair_chart(graph, use_container_width=True)

# LAYING OUT THE TOP SECTION OF THE APP
#row3_1, row3_2 = st.columns((2, 2))

#with row3_1:
    
# University selection
selected_university = st.selectbox('Choose an university to view the convocatory selected above across years and the correlation heatmap', sorted(df_year_selected['university'].unique()))

#with row3_2:
    # st.write(
    #     """
    # ##
    # Choose an university to view the scores across years and the correlation heatmap
    # """
    # )

# LAYING OUT THE MIDDLE SECTION OF THE APP
row4_1, row4_2 = st.columns((4, 1))


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
      y=alt.Y(y_axis, axis=alt.Axis(title=convocatory), scale=alt.Scale(domain=(min(df_selected_university[convocatory]) - 0.05, max(df_selected_university[convocatory]) + 0.05))),
      tooltip=convocatory).properties(title= str(uni_name_selected) + ' evolution of ' + str(convocatory) + ' scores across years')
  return st.altair_chart(chart, use_container_width=True)




with row4_1:

  #df_selected_university_year = dfs_unified[(dfs_unified['university'] == selected_university) & (dfs_unified['year'] == year_selected)]
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
    #plt.figure(figsize=(16, 4))
    heatmap = sns.heatmap(df.corr(), vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':14}, pad=12);
    st.pyplot()
  else:
    df = df_selected_university[['year', 'final_grade']]
    #plt.figure(figsize=(16, 4))
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
  
  chart = alt.Chart(df_year_selected).mark_bar().encode(
      y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
      x=alt.X('diff_1_list_final_grade:Q', axis=alt.Axis(title='Difference 1_list and final_grade'), scale=alt.Scale(domain=(min(df_year_selected['diff_1_list_final_grade']), max(df_year_selected['diff_1_list_final_grade'])))),
      tooltip=('university','diff_1_list_final_grade')
    ).properties(title = 'Difference between 1_list scores and final_grade for year ' + str(year_selected), width=200, height=600)
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
      tooltip=y_axis).properties(title = selected_university + ' ' + str(convocatory_selected)  + ' percentage difference across years')
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
  chart = alt.Chart(df_year_selected).mark_point().encode(
      x=alt.X('diff_1_list_final_grade:Q'),
      y=alt.Y('university:O'),
      color=alt.Color('CCAA:O', scale=alt.Scale(scheme='dark2'))
  )
      
  st.altair_chart(chart, use_container_width=True)



row7_1, row7_2 = st.columns((2, 2))


#with row7_1:

  # natalidad = "/Users/miguel/repos/Prediction_Medicine_Selectivity_Scores/natalidad.geojson"
  # map_data = gpd.read_file(natalidad)
  
  # # Control del tamaño de la figura del mapa
  # fig, ax = plt.subplots(figsize=(8, 8))
  
  # # Control del título y los ejes
  # ax.set_title('Natalidad por Provincias en España, 2018', 
  #             pad = 10, 
  #             fontdict={'fontsize':10, 'color': '#4873ab'})
  # ax.set_xlabel('Longitud')
  # ax.set_ylabel('Latitud')
  
  # # Añadir la leyenda separada del mapa
  # from mpl_toolkits.axes_grid1 import make_axes_locatable
  # divider = make_axes_locatable(ax)
  # cax = divider.append_axes("right", size="5%", pad=0.2)
  
  # # Generar y cargar el mapa
  # map_data.plot(column='NAT2018', cmap='plasma', ax=ax,
  #               legend=True, cax=cax, zorder=5)
  # st.pyplot(fig)



  #!pip install rioxarray
  #!pip install earthpy
  

