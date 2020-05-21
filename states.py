import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data
import streamlit as st

str_c = data.str_c
str_d = data.str_d
str_r = data.str_r
str_date = data.str_date

def main(df_sta, df_sta_cum):
    """
    Displays page showing current Covid-19 data for the different states
    of Germany. Includes the
    following elements:
        - Bar chart of total cases and deaths by state
        - Cumulative plot of all reported cases/deaths/recovered for a chosen
            state
        - Line or stacked bar chart showing daily cases/deaths/recovered since
            begin of the pandemic for a number of chosen states

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

    #

    # Site Navigation
    states_tp = tuple(sorted(list(df_sta['Bundesland'].unique())))
    st.sidebar.markdown('**  Cumulative cases over time **')
    state_sel_cum = st.sidebar.selectbox('Choose State',states_tp, 0)
    st.sidebar.markdown('**  Comparison of daily cases **')
    states_sel = st.sidebar.multiselect('Choose States',states_tp, ['Bayern'])
    # plot style for daily cases
    tr_opt1,tr_opt2 = 'Line Plot', 'Stacked Bar Plot'

    toggle_radio = st.sidebar.radio('Choose style for plot',\
                            (tr_opt1,tr_opt2))

    # bar chart showing the total number of cases and deaths in every state

    st.markdown('### Distribution of cases by states:')

    # convert data to long format
    df_sta_tot = df_sta.groupby('Bundesland').sum()[[str_c,str_d]]\
        .sort_values(by=str_c, ascending=False).reset_index()
    df_sta_tot = df_sta_tot.melt(id_vars='Bundesland', \
                    value_vars = [str_c, str_d], value_name='Cases')
    # plot
    chart_states_tot = alt.Chart(df_sta_tot)\
            .mark_bar()\
            .encode(x=alt.X('Bundesland:O', title='Bundesland', sort=list(df_sta_tot['Bundesland'].unique())),\
                    y=alt.Y('Cases:Q', title='Cumulative Cases'),\
                    color='variable',\
                   tooltip=['Cases','variable'])\
            .properties(width=800, height=600, title='Total Cases by State')
    st.write(chart_states_tot)

    # cumulative cases for specific state
    st.markdown('### Cumulative cases since begin of the pandemic:')
    st.markdown('*(Choose state in the sidebar.)*')

    chart_sta_cum = alt.Chart(data.longify_df_cum(df_sta_cum, 'Bundesland',state_sel_cum))\
            .mark_area(point=True, opacity=0.5)\
            .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                    y=alt.Y('mean(Number):Q',\
                            title='Cumulative Cases',\
                            stack=None),\
                    color='category',\
                    tooltip=['monthdate('+str_date+')','category','Number'])\
            .properties(width=800, height=400, title='Number of cases in '+state_sel_cum)
    st.write(chart_sta_cum)

    # plot the current daily new cases as a stacked bar Plot
    # or a line plot
    st.markdown('### Daily cases since begin of the pandemic:')
    st.markdown('*(Choose states to compare and plot style in the sidebar.)*')

    if toggle_radio == tr_opt1:
        #st.markdown('Line Chart:')
        chart_sta_day = \
        alt.Chart(df_sta.loc[df_sta['Bundesland'].isin(states_sel)])\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                    y=alt.Y('mean('+str_c+'):Q', title='Cumulative Cases'),\
                    color='Bundesland',\
                    tooltip=['Bundesland',str_c])\
                .properties(width=800, height=400, title='Reported cases per day')\
            .interactive()
    elif toggle_radio == tr_opt2:
        #st.text('Numbers stacked on top.')
        chart_sta_day = alt.Chart(df_sta.loc[df_sta['Bundesland'].isin(states_sel)])\
            .mark_bar(point=True)\
            .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                    y=alt.Y('mean('+str_c+'):Q', title='Cumulative Cases'),\
                    color='Bundesland',\
                    tooltip=['Bundesland',str_c])\
            .properties(width=800, height=400, title='Reported cases per day')\
            .interactive()
    st.write(chart_sta_day)
