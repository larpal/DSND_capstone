import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data
import numpy as np


#def country_main(df_ctr_cum,df_ctr,_width=800,_height=500):
def main():

    df_ctr_cum = data.df_ctr_cum
    df_ctr = data.df_ctr
    #df_cases = data.df_cases
    df_stats = data.df_stats
    df_loc = data.df_cases_loc_long
    _width = data._width
    _height = data._height

    #st.write(df_ctr_cum )
    # Overview


    st.table(df_stats.set_index(' '))

    map_navigation = \
        st.sidebar.radio('Display cases on map',\
                                ('Total Cases','Past 7 days'))

    if map_navigation == 'Total Cases':
        map_data = df_loc[['lat','lon']]
    elif map_navigation == 'Past 7 days':
        map_data = df_loc.loc[(pd.Timestamp.today() - df_loc['Meldedatum']).dt.days < 7][['lat','lon']]


    st.deck_gl_chart(
    viewport={
        'latitude': 54.32,
         'longitude': 10.1,
         'zoom': 3,
        'pitch': 40,
        },
    layers=[{
        'type': 'HexagonLayer',
        'data': map_data,
        'radius': 10000,
        'elevationScale': 4,
        'elevationRange': [0, 5000],
        'pickable': True,
        'extruded': True,
        }
        ,{
        'type': 'ScatterplotLayer',
            'data': map_data,
            }
        ])

    toggle_log_cum_chart = st.checkbox('Logarithmic Cumulative Cases')

    if toggle_log_cum_chart:
        # logarithmic plot
        c2 = alt.Chart(df_ctr_cum)\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', title='Cumulative Cases',\
                            scale=alt.Scale(type='log')), color='category',\
                            tooltip=['monthdate(Meldedatum)','Number'])\
            .properties(width=_width, height=_height, title='Number of Cases')
    else:
        # linear plot
        c2 = alt.Chart(df_ctr_cum)\
            .mark_area(point=False, opacity=0.6)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q',\
                            title='Cumulative Cases',\
                            stack=None),\
                    color='category',\
                    tooltip=['monthdate(Meldedatum)','category','Number'])\
            .properties(width=_width, height=_height, title='Number of Cases')

    st.write(c2)


    # second chart
    toggle_log_daily_chart = st.checkbox('Logarithmic Daily Cases')

    if toggle_log_daily_chart == False:
        chart_daily_cases = \
        alt.Chart(df_ctr)\
            .mark_bar(point=True)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', title='Cumulative Cases'),\
                    color='category',\
                    tooltip=['monthdate(Meldedatum)','Number'])\
            .properties(width=800, height=400, title='Number of Cases')
    else:
        chart_daily_cases = \
        alt.Chart(df_ctr.loc[df_ctr['Number']>0])\
        .mark_line(point=True)\
        .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                y=alt.Y('mean(Number):Q', title='Cumulative Cases',\
                       scale=alt.Scale(type='log')),\
                color='category',\
                tooltip=['monthdate(Meldedatum)','Number'])\
        .properties(width=800, height=400, title='Number of Cases')
    st.write(chart_daily_cases)
