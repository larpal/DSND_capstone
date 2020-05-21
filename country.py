import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data
import numpy as np


def main(df_stats, df_deaths_stats, df_ctr, df_ctr_cum):

    #df_ctr_cum = data.df_ctr_cum
    #df_ctr = data.df_ctr
    #df_cases = data.df_cases
    #df_stats = data.df_stats
    #df_death_stats = data.df_death_stats

    _width = data._width
    _height = data._height

    # Overview
    st.markdown('### Current stats for '+pd.Timestamp.today().strftime('%B %d, %Y')+':')
    st.table(df_stats)


    st.markdown('### Total number of deaths for different age groups:')

    chart_age_dist = alt.Chart(df_deaths_stats).mark_bar()\
    .encode(x=alt.X('Age'),\
            y=alt.Y('Count',scale=alt.Scale(type='log')),\
            tooltip = ['Age', 'Count']).\
    properties(width = _width*3/4, height = _height/2, title='Log Number of Deaths in Different Age Groups')
    st.write(chart_age_dist)

    # cumulative cases chart
    st.markdown('### Cumulative cases since begin of the pandemic:')
    toggle_log_cum_chart = st.checkbox('Logarithmic Cumulative Cases')



    if toggle_log_cum_chart:
        # logarithmic plot
        chart_cum_cases = alt.Chart(df_ctr_cum)\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', title='Cumulative Cases',\
                            scale=alt.Scale(type='log')), color='category',\
                            tooltip=['monthdate(Meldedatum)','category','Number'])\
            .properties(width=_width, height=_height, title='Number of Cases')
    else:
        # linear plot
        chart_cum_cases = alt.Chart(df_ctr_cum)\
            .mark_area(point=False, opacity=0.6)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q',\
                            title='Cumulative Cases',\
                            stack=None),\
                    color='category',\
                    tooltip=['monthdate(Meldedatum)','category','Number'])\
            .properties(width=_width, height=_height, title='Number of Cases')

    st.write(chart_cum_cases)


    # daily cases chart
    st.markdown('### Daily cases since begin of the pandemic:')
    toggle_log_daily_chart = st.checkbox('Logarithmic Daily Cases')


    if toggle_log_daily_chart == False:
        chart_daily_cases = \
        alt.Chart(df_ctr)\
            .mark_bar(point=True)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', title='Cumulative Cases'),\
                    color='category',\
                    tooltip=['monthdate(Meldedatum)','category','Number'])\
            .properties(width=800, height=400, title='Number of Cases')
    else:
        chart_daily_cases = \
        alt.Chart(df_ctr.loc[df_ctr['Number']>0])\
        .mark_line(point=True)\
        .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                y=alt.Y('mean(Number):Q', title='Cumulative Cases',\
                       scale=alt.Scale(type='log')),\
                color='category',\
                tooltip=['monthdate(Meldedatum)','category','Number'])\
        .properties(width=800, height=400, title='Number of Cases')
    st.write(chart_daily_cases)


def show_map(df_loc):

    #df_loc = data.df_cases_loc_long
    st.markdown('### Regional distribution of recorded COVID-19 cases:')

    map_navigation = \
        st.radio('Choose cases to display on map',\
                                ('Total Cases','Past 7 days'))

    if map_navigation == 'Total Cases':
        map_data = df_loc[['lat','lon']].astype(float)
    elif map_navigation == 'Past 7 days':
        map_data = df_loc.loc[(pd.Timestamp.today() - df_loc['Meldedatum']).dt.days < 7][['lat','lon']].astype(float)


    #st.write(map_data.astype(float))
    #st.map(map_data[['lat','lon']].astype(float).head(100))

    st.deck_gl_chart(
    viewport={
        'latitude': 54.32,
         'longitude': 10.1,
         'zoom': 4,
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
