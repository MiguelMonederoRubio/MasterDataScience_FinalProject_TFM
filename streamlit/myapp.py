# in terminal: streamlit run /Users/miguel/repos/Spain_Medicine_Admissions_App/streamlit/myapp.py

import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import altair as alt
import folium as folium  # pip install folium
from streamlit_folium import folium_static # pip install streamlit-folium



# load data from notebook
your_directory = '/Users/miguel'
exported_data_directory = your_directory + '/output'
file_name = exported_data_directory + '/exported_data_notebook.csv'
dfs_unified = pd.read_csv(file_name)

# functions we are going to use below

# bar chart
def bar_chart(df, x_axis):
  chart = alt.Chart(df).mark_bar().encode(
  x=alt.X(x_axis, axis=alt.Axis(title=score_selected), scale=alt.Scale(domain=(min(df[score_selected]) - 0.05, max(df[score_selected]) + 0.05))),
  y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
  color=alt.condition(
    alt.datum.highlight_color == 'yes', 
    alt.value('orange'),     # highlight bars
    alt.value('gray')   # And grey for the rest of the bars
  ),
  tooltip=('university',score_selected)
  )
  return chart

# create markers in map
def create_marker(map, latitude, longitude, popup_info, tooltip_info, color_marked):
   folium.Marker(
      location=[latitude, longitude], # coordinates for the marker (Earth Lab at CU Boulder)
      popup=popup_info, # pop-up label for the marker,
      tooltip=tooltip_info , # tooltip label for the marker
      icon=folium.Icon(color=color_marked, icon='university', prefix='fa', icon_color='white')
      ).add_to(map)


# wide mode
st.set_page_config(layout="wide")


# LAYING OUT THE APP IN SECTIONS
row1_1, row1_2 = st.columns((2, 2))

with row1_1:
  st.title("Spain's Medicine Admissions App")

with row1_2:
  st.write(
    """
    Displayed are the access scores of public universities in Spain to study medicine. Two scores are shown:
    - "1_list": first score published. This is the highest score to be admitted at a university
    - "final_grade": last score published. This is the lowest score to be admitted at a university
    *Scores shown for 2022 are predicted scores calculated by a Machine Learning model.
    """
    )

# LAYING OUT THE APP IN SECTIONS
row2_1, row2_2, row2_3, row2_4 = st.columns((3, 1, 1, 1))

with row2_1:
  year_selected = st.slider("Select year", 2022, 2010)




# df filtered by year
df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected)]


with row2_2:
  # selectbox to filter by CCAA (commmunities of Spain)
  CCAA = list(df_year_selected['CCAA'].unique())
  CCAA.append('All')
  CCAA_selected = st.selectbox('Filter by CCAA (optional)', sorted(CCAA))



with row2_3:
  # filter by score
  score_introduced = st.text_input('Filter by score (optional) (e.g., 12.5)')

# errors to be shown on the filter by score
  if (score_introduced == ''):
    pass
  else:
    try:
      float(score_introduced)
    except ValueError:
      st.error('Please enter a number')
      score_introduced = ''
  
  if (score_introduced == ''):
    pass
  elif float(score_introduced) > float(14):
    st.error('Please enter a number between 0 and 14')
  elif float(score_introduced) < float(0):
    st.error('Please enter a number between 0 and 14')


# list of the 2 scores
score = ['final_grade', '1_list']

with row2_4:
  score_selected = st.radio('Select  score', score)
  

# LAYING OUT THE APP IN SECTIONS
row3_1, row3_2 = st.columns((2, 2))

# create different dfs based on the filters used
if (CCAA_selected == 'All') & (score_introduced == ''):
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected)]
  
elif (CCAA_selected != 'All') & (score_introduced == ''):
  df_year_selected_CCAA = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified['CCAA'] == CCAA_selected)]
  list_unis_year_selected_CCAA = list(df_year_selected_CCAA['university'])
elif (CCAA_selected == 'All') & (score_introduced != ''):
  df_year_selected_score = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified[score_selected] <= float(score_introduced))]
  list_unis_year_selected_score = list(df_year_selected_score['university'])
else:
  # (CCAA_selected != 'All') & (score_introduced != '')
  df_year_selected_CCAA_score = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified['CCAA'] == CCAA_selected) & (dfs_unified[score_selected] <= float(score_introduced))]
  list_unis_year_selected_CCAA_score = list(df_year_selected_CCAA_score['university'])

with row3_1:

# bar chart
  if score_selected == '1_list':
    x_axis = '1_list:Q'
  else:
    x_axis = 'final_grade:Q'
  
  # to color universities based on filters
  df_year_selected['highlight_color'] = ''
  if (CCAA_selected != 'All') & (score_introduced == ''):
    for uni in list_unis_year_selected_CCAA:
      df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])
    chart = bar_chart(df_year_selected, x_axis)
  elif (CCAA_selected != 'All') & (score_introduced != ''):
    for uni in list_unis_year_selected_CCAA_score:
      df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])
    chart = bar_chart(df_year_selected, x_axis)
  elif (CCAA_selected == 'All') & (score_introduced != ''):
    for uni in list_unis_year_selected_score:
      df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])
    chart = bar_chart(df_year_selected, x_axis)
  else:
      chart = alt.Chart(df_year_selected).mark_bar().encode(
          x=alt.X(x_axis, axis=alt.Axis(title=score_selected), scale=alt.Scale(domain=(min(df_year_selected[score_selected]) - 0.05, max(df_year_selected[score_selected]) + 0.05))),
          y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
          tooltip=('university',score_selected)
        )
    
  text = chart.mark_text(
    align='left',
    baseline='middle',
    color='white',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
  ).encode(
    text=x_axis
  )

  graph = (chart + text).properties(title= str(year_selected) + ' ' + score_selected + ' scores', width=200, height=600)
    
  st.altair_chart(graph, use_container_width=True)






  
  # to color universities based on filters
  # df_year_selected['highlight_color'] = ''
  # if (CCAA_selected != 'All') & (score_introduced == ''):
  #   for uni in list_unis_year_selected_CCAA:
  #     df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])

  #   chart = alt.Chart(df_year_selected).mark_bar().encode(
  #   x=alt.X(x_axis, axis=alt.Axis(title=score_selected), scale=alt.Scale(domain=(min(df_year_selected[score_selected]) - 0.05, max(df_year_selected[score_selected]) + 0.05))),
  #   y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
  #   color=alt.condition(
  #     alt.datum.highlight_color == 'yes', 
  #     alt.value('orange'),     # highlight bars
  #     alt.value('gray')   # And grey for the rest of the bars
  #   ),
  #   tooltip=('university',score_selected)
  #   )
  # elif (CCAA_selected != 'All') & (score_introduced != ''):
  #   for uni in list_unis_year_selected_CCAA_score:
  #     df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])
  #   chart = alt.Chart(df_year_selected).mark_bar().encode(
  #   x=alt.X(x_axis, axis=alt.Axis(title=score_selected), scale=alt.Scale(domain=(min(df_year_selected[score_selected]) - 0.05, max(df_year_selected[score_selected]) + 0.05))),
  #   y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
  #   color=alt.condition(
  #     alt.datum.highlight_color == 'yes', 
  #     alt.value('orange'),     # highlight bars
  #     alt.value('gray')   # And grey for the rest of the bars
  #   ),
  #   tooltip=('university',score_selected)
  #   )
  # elif (CCAA_selected == 'All') & (score_introduced != ''):
  #   for uni in list_unis_year_selected_score:
  #     df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])
  #   chart = alt.Chart(df_year_selected).mark_bar().encode(
  #   x=alt.X(x_axis, axis=alt.Axis(title=score_selected), scale=alt.Scale(domain=(min(df_year_selected[score_selected]) - 0.05, max(df_year_selected[score_selected]) + 0.05))),
  #   y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
  #   color=alt.condition(
  #     alt.datum.highlight_color == 'yes', 
  #     alt.value('orange'),     # highlight bars
  #     alt.value('gray')   # And grey for the rest of the bars
  #   ),
  #   tooltip=('university',score_selected)
  #   )
  # else:
  #     chart = alt.Chart(df_year_selected).mark_bar().encode(
  #         x=alt.X(x_axis, axis=alt.Axis(title=score_selected), scale=alt.Scale(domain=(min(df_year_selected[score_selected]) - 0.05, max(df_year_selected[score_selected]) + 0.05))),
  #         y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
  #         tooltip=('university',score_selected)
  #       )
    
  # text = chart.mark_text(
  #   align='left',
  #   baseline='middle',
  #   color='white',
  #   dx=3  # Nudges text to right so it doesn't appear on top of the bar
  # ).encode(
  #   text=x_axis
  # )

  # graph = (chart + text).properties(title= str(year_selected) + ' ' + score_selected + ' scores', width=200, height=600)
    
  # st.altair_chart(graph, use_container_width=True)






with row3_2:

  f = folium.Figure(width=800, height=550)

# change latitude, longitude and zoom of map based on CCAA selected
# latitude and longitude below are values to have each CCAA centered on the map

  if CCAA_selected == 'All':
    latitude_map = 40.4167047
    longitude_map = -3.7035825
    zoom_map = 6
  elif CCAA_selected == 'C. Madrid':
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
  elif CCAA_selected == 'C. Valenciana':
    latitude_map = 39.4786642
    longitude_map = -0.3627246
    zoom_map = 8
  elif CCAA_selected == 'Asturias':
    latitude_map = 43.3533657
    longitude_map = -5.8687712
    zoom_map = 8
  elif CCAA_selected == 'Islas Baleares':
    latitude_map = 39.60701435
    longitude_map = 2.64475448
    zoom_map = 8
  elif CCAA_selected == 'Navarra':
    latitude_map = 42.8154264
    longitude_map = -1.65263107
    zoom_map = 8
  elif CCAA_selected == 'Murcia':
    latitude_map = 38.02023375
    longitude_map = -1.16866755
    zoom_map = 8
  else:
    latitude_map = 40.4167047
    longitude_map = -3.7035825
    zoom_map = 6

  m = folium.Map(location=[latitude_map, longitude_map], zoom_start=zoom_map, width=800, height=550, control_scale=True, tiles='CartoDB Positron',
                  name='Light Map', attr='My Data attribution').add_to(f)


  
  #list_unis_year_selected = list(df_year_selected['university'].unique())
  list_unis_year_selected = list(df_year_selected['university'])
  # iterate through list
 
  for uni in list_unis_year_selected:
    latitude_uni = df_year_selected.loc[df_year_selected['university'] == uni, 'latitude'].mean()
    longitude_uni = df_year_selected.loc[df_year_selected['university'] == uni, 'longitude'].mean()
    
    score = df_year_selected.loc[df_year_selected['university'] == uni, score_selected].mean()
    
    uni_highlighted = list(df_year_selected.loc[df_year_selected['highlight_color'] == 'yes', 'university'])

    if uni in uni_highlighted:
      color_marked = 'orange'
    else:
      color_marked = 'lightgray'

    if (CCAA_selected == 'All') & (score_introduced == ''):
      color_marked = 'blue'
    
    create_marker(m, latitude_uni, longitude_uni, uni + ': ' + str(score), uni + ': ' + str(score), color_marked)
  
  # Display the map
  folium_static(f, width=800, height=550)






# scores by CCAA
df_CCAA_year_selected = df_year_selected.groupby('CCAA')[score_selected].mean().reset_index()
# round to 3 decimals
df_CCAA_year_selected[score_selected] = df_CCAA_year_selected[score_selected].apply(lambda x: round(x, 3))

# bar chart
if score_selected == '1_list':
    y_axis = '1_list:Q'
else:
    y_axis = 'final_grade:Q'


# to color universities filtered
if (CCAA_selected != 'All'):
  df_CCAA_year_selected['highlight_color'] = ''
  df_CCAA_year_selected['highlight_color'] = np.where(df_CCAA_year_selected['CCAA'] == CCAA_selected, 'yes', df_CCAA_year_selected['highlight_color'])
  
  chart = alt.Chart(df_CCAA_year_selected).mark_bar().encode(
    x=alt.X('CCAA:O', sort='-y', axis=alt.Axis(title='CCAA', labelAngle=0)),
    y=alt.Y(y_axis, axis=alt.Axis(title=score_selected), scale=alt.Scale(domain=(min(df_CCAA_year_selected[score_selected]) - 0.05, max(df_CCAA_year_selected[score_selected]) + 0.05))),
    color=alt.condition(
      alt.datum.highlight_color == 'yes', 
      alt.value('orange'),     # highlight bars
      alt.value('gray')   # And grey for the rest of the bars
    ),
    tooltip=('CCAA',score_selected)
  )

else:
  chart = alt.Chart(df_CCAA_year_selected).mark_bar().encode(
    x=alt.X('CCAA:O', sort='-y', axis=alt.Axis(title='CCAA', labelAngle=0)),
    y=alt.Y(y_axis, axis=alt.Axis(title=score_selected), scale=alt.Scale(domain=(min(df_CCAA_year_selected[score_selected]) - 0.05, max(df_CCAA_year_selected[score_selected]) + 0.05))),
    tooltip=('CCAA',score_selected)
  )

text = chart.mark_text(
    align='center',
    baseline='bottom',
    color='white',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
  ).encode(
    text=y_axis,  
  )
    
graph = (chart + text).properties(title= str(year_selected) + ' average ' + score_selected + ' scores by CCAA', width = 200, height = 400)
  
st.altair_chart(graph, use_container_width=True)




st.write(
  """
  Some people get admitted to an university they applied for but they decide to switch to another university, making the access score of the university they are leaving go down. Which university and CCAA experience the biggest difference between the 1_list and the final_grade scores?
  """
  )

# LAYING OUT THE APP IN SECTIONS
row4_1, row4_2 = st.columns((2, 2))

# diff between 1_list and final_grade column

with row4_1:
  
  # bar chart
  if (CCAA_selected != 'All') & (score_introduced == ''):
    for uni in list_unis_year_selected_CCAA:
      df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])
      
    chart = alt.Chart(df_year_selected).mark_bar().encode(
    y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
    x=alt.X('diff_1_list_final_grade:Q', axis=alt.Axis(title='Difference 1_list and final_grade'), scale=alt.Scale(domain=(min(df_year_selected['diff_1_list_final_grade']), max(df_year_selected['diff_1_list_final_grade']) + 0.01))),
    color=alt.condition(
      alt.datum.highlight_color == 'yes', 
      alt.value('orange'),     # highlight bars
      alt.value('gray')   # And grey for the rest of the bars
    ),tooltip=('university','diff_1_list_final_grade')
    )
  elif (CCAA_selected != 'All') & (score_introduced != ''):
    for uni in list_unis_year_selected_CCAA_score:
      df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])
      
    chart = alt.Chart(df_year_selected).mark_bar().encode(
    y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
    x=alt.X('diff_1_list_final_grade:Q', axis=alt.Axis(title='Difference 1_list and final_grade'), scale=alt.Scale(domain=(min(df_year_selected['diff_1_list_final_grade']), max(df_year_selected['diff_1_list_final_grade']) + 0.01))),
    color=alt.condition(
      alt.datum.highlight_color == 'yes', 
      alt.value('orange'),     # highlight bars
      alt.value('gray')   # And grey for the rest of the bars
    ),tooltip=('university','diff_1_list_final_grade')
    )
  elif (CCAA_selected == 'All') & (score_introduced != ''):
    for uni in list_unis_year_selected_score:
      df_year_selected['highlight_color'] = np.where(df_year_selected['university'] == uni, 'yes', df_year_selected['highlight_color'])
        
      chart = alt.Chart(df_year_selected).mark_bar().encode(
      y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
      x=alt.X('diff_1_list_final_grade:Q', axis=alt.Axis(title='Difference 1_list and final_grade'), scale=alt.Scale(domain=(min(df_year_selected['diff_1_list_final_grade']), max(df_year_selected['diff_1_list_final_grade']) + 0.01))),
      color=alt.condition(
        alt.datum.highlight_color == 'yes', 
        alt.value('orange'),     # highlight bars
        alt.value('gray')   # And grey for the rest of the bars
      ),tooltip=('university','diff_1_list_final_grade')
      )
  else:
    chart = alt.Chart(df_year_selected).mark_bar().encode(
      y=alt.Y('university:O', sort='-x', axis=alt.Axis(title='University')),
      x=alt.X('diff_1_list_final_grade:Q', axis=alt.Axis(title='Difference 1_list and final_grade'), scale=alt.Scale(domain=(min(df_year_selected['diff_1_list_final_grade']), max(df_year_selected['diff_1_list_final_grade']) + 0.01))),
      tooltip=('university','diff_1_list_final_grade')
    )
  
  
  text = chart.mark_text(
    align='left',
    baseline='middle',
    color='white',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
  ).encode(
    text='diff_1_list_final_grade:Q'
  )

  graph = (chart + text).properties(title = 'Difference between 1_list scores and final_grade for year ' + str(year_selected), width=200, height=600)
    
  st.altair_chart(graph, use_container_width=True)


with row4_2:
  # bar chart
  df_CCAA_year_selected_diff = df_year_selected.groupby('CCAA')['diff_1_list_final_grade'].mean().reset_index()
  # round to 3 decimals
  df_CCAA_year_selected_diff['diff_1_list_final_grade'] = df_CCAA_year_selected_diff['diff_1_list_final_grade'].apply(lambda x: round(x, 3))
  df_CCAA_year_selected_diff['highlight_color'] = ''
  df_CCAA_year_selected_diff['highlight_color'] = np.where(df_CCAA_year_selected_diff['CCAA'] == CCAA_selected, 'yes', df_CCAA_year_selected_diff['highlight_color'])

  if (CCAA_selected != 'All'):
    chart = alt.Chart(df_CCAA_year_selected_diff).mark_bar().encode(
        y=alt.Y('CCAA:O', sort='-x', axis=alt.Axis(title='CCAA')),
        x=alt.X('diff_1_list_final_grade:Q', axis=alt.Axis(title='Difference 1_list and final_grade'), scale=alt.Scale(domain=(min(df_CCAA_year_selected_diff['diff_1_list_final_grade']), max(df_CCAA_year_selected_diff['diff_1_list_final_grade']) + 0.01))),
        color=alt.condition(
          alt.datum.highlight_color == 'yes', 
          alt.value('orange'),     # highlight bars
          alt.value('gray')   # And gray for the rest of the bars
        ),tooltip=('CCAA','diff_1_list_final_grade')
      )
  else:
    chart = alt.Chart(df_CCAA_year_selected_diff).mark_bar().encode(
        y=alt.Y('CCAA:O', sort='-x', axis=alt.Axis(title='CCAA')),
        x=alt.X('diff_1_list_final_grade:Q', axis=alt.Axis(title='Difference 1_list and final_grade'), scale=alt.Scale(domain=(min(df_CCAA_year_selected_diff['diff_1_list_final_grade']), max(df_CCAA_year_selected_diff['diff_1_list_final_grade']) + 0.01))),
        tooltip=('CCAA','diff_1_list_final_grade')
      )

  text = chart.mark_text(
      align='left',
      baseline='middle',
      color='white',
      dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
      text='diff_1_list_final_grade:Q'
    )
      
  graph = (chart + text).properties(title = 'Difference between 1_list scores and final_grade for year ' + str(year_selected) + ' by CCAA', width=200, height=600)
    
  st.altair_chart(graph, use_container_width=True)





st.write(
  """
  Historical view of the scores (score selected above) for a specific university
  """
  )
# University selection
if (CCAA_selected == 'All') & (score_introduced == ''):
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected)]
elif (CCAA_selected != 'All') & (score_introduced == ''):
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified['CCAA'] == CCAA_selected)]
elif (CCAA_selected == 'All') & (score_introduced != ''):
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified[score_selected] <= float(score_introduced))]
else:
  #(CCAA_selected != 'All') & (score_introduced != '')
  df_year_selected = dfs_unified[(dfs_unified['year'] == year_selected) & (dfs_unified['CCAA'] == CCAA_selected) & (dfs_unified[score_selected] <= float(score_introduced))]
  

selected_university = st.selectbox('Select an university', sorted(df_year_selected['university'].unique()))

# LAYING OUT THE APP IN SECTIONS
row5_1, row5_2 = st.columns((4, 1))
with row5_1:
  
  # line chart 1_list and final_grade

  def line_chart_selected_uni(uni_name_selected, score):
    #create y_axis name
    if score == 'final_grade':
        y_axis = 'final_grade:Q'
    else:
        y_axis = '1_list:Q'
    # filter by university
    df_selected_university = dfs_unified[(dfs_unified['university'] == uni_name_selected)]
    # chart

    if (CCAA_selected != 'All') | (score_introduced != ''):
      chart = alt.Chart(df_selected_university).mark_line(point=True).encode(
          x=alt.X('year:N', axis=alt.Axis(title='Year', labelAngle=0)),
          y=alt.Y(y_axis, axis=alt.Axis(title=score), scale=alt.Scale(domain=(min(df_selected_university[score]) - 0.1, max(df_selected_university[score]) + 0.1))),
          color=alt.value('orange'),
          tooltip=score)
    else:
      chart = alt.Chart(df_selected_university).mark_line(point=True).encode(
          x=alt.X('year:N', axis=alt.Axis(title='Year', labelAngle=0)),
          y=alt.Y(y_axis, axis=alt.Axis(title=score), scale=alt.Scale(domain=(min(df_selected_university[score]) - 0.1, max(df_selected_university[score]) + 0.1))),
          tooltip=score)
    
    text = chart.mark_text(
        align='center',
        baseline='bottom',
        color='white',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
      ).encode(
        text= y_axis
      )
      
    graph = (chart + text).properties(title= str(uni_name_selected) + ' evolution of ' + str(score) + ' scores across years')
    
    return st.altair_chart(graph, use_container_width=True)

  try:
    line_chart_selected_uni(selected_university, score_selected)
  except:
    st.error('No universities available given the filters entered')
 

with row5_2:
  st.set_option('deprecation.showPyplotGlobalUse', False)
  df_selected_university = dfs_unified[(dfs_unified['university'] == selected_university)]
  df_selected_university_reduced = df_selected_university[['year', score_selected]]
  heatmap = sns.heatmap(df_selected_university_reduced.corr(), vmax=1, annot=True, cmap='BrBG')
  heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':14}, pad=12);
  st.pyplot()

  

# AUTHOR INFORMATION

st.write(
    """
    Author: Miguel Monedero Rubio

    Linkedin: https://es.linkedin.com/in/miguel-monedero-rubio-9abb73150

    Github: https://github.com/MiguelMonederoRubio
    """
    )