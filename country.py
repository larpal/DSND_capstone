import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data
import pydeck as pdk

str_date = data.str_date
str_c = data.str_c
str_d = data.str_d
str_r = data.str_r


def main(df_stats, df_deaths_stats, df_ctr, df_ctr_cum):
    """
    Displays page showing current Covid-19 data for Germany. Includes the
    following elements:
        - Show table with stats for current day
        - Bar chart showing age distribution of deaths
        - Cumulative plot of all reported cases/deaths/recovered
        - Bar chart showing daily cases/deaths/recovered since begin of the
          pandemic
    Args: all of the below data frames are outputs of etl_main in the etl
    module. See this module for reference.
        - df_stats: data frame containing stats for current day
        - df_deaths_stats: data frame containing number of deaths by age group
        - df_ctr: data frame containing daily data for Germany
        - df_ctr_cum: data frame containing cumulative daily data for Germany
    Returns: None
    """
    # get plot properties
    _width = data._width
    _height = data._height
    st.markdown('**All numbers and charts on this page are for Germany as a whole.**')
    # Overview
    st.markdown('### Current stats for '+\
                pd.Timestamp.today().strftime('%B %d, %Y')+':')
    st.table(df_stats)

    st.markdown('### Total number of deaths for different age groups:')

    # Bar chart showing deaths by age group
    chart_age_dist = alt.Chart(df_deaths_stats).mark_bar()\
    .encode(x=alt.X('Age'),\
            y=alt.Y('Count',scale=alt.Scale(type='log')),\
            tooltip = ['Age', 'Count']).\
    properties(width = _width*3/4, height = _height/2, \
                title='Log number of Covid-19 deaths in Germany by age')
    st.write(chart_age_dist)

    # Area chart showing cumulative cases
    st.markdown('### Cumulative cases since begin of the pandemic:')
    toggle_log_cum_chart = st.checkbox('Logarithmic cumulative cases')

    if toggle_log_cum_chart:
        # logarithmic plot
        chart_cum_cases = alt.Chart(df_ctr_cum)\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', \
                            title='Cumulative Reported Cases',\
                            scale=alt.Scale(type='log')), color='category',\
                            tooltip=['monthdate('+str_date+')',\
                                        'category','Number'])\
            .properties(width=_width, height=_height, \
                        title='Log total cases in Germany')
    else:
        # linear plot
        chart_cum_cases = alt.Chart(df_ctr_cum)\
            .mark_area(point=False, opacity=0.6)\
            .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                    y=alt.Y('mean(Number):Q',\
                            title='Cumulative Reported Cases',\
                            stack=None),\
                    color='category',\
                    tooltip=['monthdate('+str_date+')','category','Number'])\
            .properties(width=_width, height=_height, \
                        title='Total cases in Germany')

    st.write(chart_cum_cases)


    #### Add predictions ####
    st.markdown('### Current trend with predictions:')
    #st.write(data.predict_days(df_ctr_cum, 14, 3, str_c))
    df_predicted = pd.concat([data.predict_days(df_ctr_cum, 14, 3, str_c),\
                          data.predict_days(df_ctr_cum, 14, 3, str_d),\
                          data.predict_days(df_ctr_cum, 14, 3, str_r)])
    chart_cum_cases1 = alt.Chart(df_ctr_cum.iloc[-3*14:])\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', \
                            title='Cumulative Reported Cases'), color='category',\
                            tooltip=['monthdate('+str_date+')',\
                                        'category','Number'])\

    chart_predictions = alt.Chart(df_predicted)\
            .mark_point()\
            .encode(x=alt.X('monthdate('+'date'+'):O'),\
                    y=alt.Y('predictions:Q'), color='category',\
                            tooltip=['monthdate('+'date'+')',\
                                        'predictions'])
    chart_cum_pred = (chart_cum_cases1+chart_predictions)\
                .properties(width=_width, height=_height, \
                    title='Recent days and 3-day ahead predictions')

    st.write(chart_cum_pred)
    # Stacked bar chart showing daily cases
    st.markdown('### Daily cases since begin of the pandemic:')
    toggle_log_daily_chart = st.checkbox('Logarithmic daily cases')

    if toggle_log_daily_chart == False:
        chart_daily_cases = \
        alt.Chart(df_ctr)\
            .mark_bar(point=True)\
            .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', title='Reported Cases'),\
                    color='category',\
                    tooltip=['monthdate('+str_date+')','category','Number'])\
            .properties(width=800, height=400, title='Daily cases in Germany')
    else:
        chart_daily_cases = \
        alt.Chart(df_ctr.loc[df_ctr['Number']>0])\
        .mark_line(point=True)\
        .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                y=alt.Y('mean(Number):Q', title='Reported Cases',\
                       scale=alt.Scale(type='log')),\
                color='category',\
                tooltip=['monthdate('+str_date+')','category','Number'])\
        .properties(width=800, height=400, title='Log daily cases in Germany')
    st.write(chart_daily_cases)


def show_map(df_loc):
    """
    Displays page showing map of Germany and an overaly heat map
    with number of reported Covid-19 cases for per 100k inhabitants
    each district in Germany. Can choose between
        - heatmap of all cases (per 100k) since begin of pandemic
        - heatmap of cases (per 100k) in the past 7 days.

    Args: the below data frame is an output of etl_main in the etl
    module. See this module for reference.
        - df_loc: data frame containing coordinates and date for each
            reported Covid-19 case
    Returns: None
    """

    st.markdown('### Regional distribution of recorded COVID-19 cases '+\
                'per 100.000 inhabitants.')
    st.markdown('*Note: colors indicate number of reported cases '+\
                'relative to the district with the largest number.*')

    map_navigation = \
        st.radio('Choose cases to display on map:',\
                                ('Since begin of pandemic','Past 7 days'))

    # Pull coordinates
    if map_navigation == 'Since begin of pandemic':
        map_data = df_loc[['lat','lon']].astype(float)
    elif map_navigation == 'Past 7 days':
        map_data = df_loc.loc[(pd.Timestamp.today() - \
                                df_loc[str_date]).dt.days < 7]\
                                [['lat','lon']].astype(float)


    layer = pdk.Layer(
    "HexagonLayer",\
    map_data,\
    get_position=["lon", "lat"],\
    auto_highlight=True,\
    elevation_scale=4,\
    radius= 10000,\
    pickable=True,\
    elevation_range=[0, 5000],\
    extruded=True,\
    coverage=1,\
    )
    view_state = pdk.ViewState(
    longitude=9.21, latitude=50.32, \
    zoom=4, pitch=40,
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
