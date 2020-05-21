import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data


str_c = data.str_c
str_d = data.str_d
str_r = data.str_r
str_dstrct = data.str_dstrct
str_date = data.str_date

def main(df_lkr, df_cases_rolling):
    """
    Displays page showing current Covid-19 data for the different districts
    of Germany. Includes the following elements for a chosen number of districts:
        - Line chart showing rolling sum of the past 7 days' cases per 100k
        inhabitants
        - Stacked bar plot showing the daily number of reported cases

    Args: all of the below data frames are outputs of etl_main in the etl
    module. See this module for reference.
        - df_lkr: data frame containing stats for current day
        - df_cases_rolling: data frame containing number of deaths by age group
    Returns: None
    """
    # get plot properties
    _width = data._width
    _height = data._height

    df_lkr_roll = \
            pd.melt(df_cases_rolling, id_vars=[str_date, str_dstrct],\
                    value_vars = ['AnzahlFall100k'],\
                    var_name = 'category',\
                    value_name = 'cases')

    st.markdown('*Choose any number of districts in the sidebar.*')



    lkr_tp = tuple(sorted(list(df_lkr[str_dstrct].unique())))
    lkr_sel = st.sidebar.multiselect('Choose Districts',lkr_tp,['SK Hamburg'])

    # chart displaying rolling sum of cases in the past week
    st.markdown('### Rolling sum of cases over past 7 days:')
    st.markdown('*Normalized to number of cases per 100.000 inhabitants.'+\
        ' The red line indicates 50 new cases per 100.000 inhabitants within '+\
        'a week which is considered a threshold for further lockdown measures. *')
    line_data = pd.DataFrame({'a': [50]})
    # line at 50 cases
    chart_line = alt.Chart(line_data).mark_rule(strokeWidth=10).encode(y='a:Q',\
                                            opacity=alt.value(0.2),
                                            color = alt.value('red'))
    chart_cases_per_100k = \
    alt.Chart(df_lkr_roll.loc[df_lkr_roll[str_dstrct].isin(lkr_sel)])\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                    y=alt.Y('mean(cases):Q', title='Cases'),\
                    color=str_dstrct,\
                   tooltip = [str_dstrct,str_date,'cases'])
    chart_100k = (chart_cases_per_100k+chart_line).properties\
    (width=800, height=400, title='Rolling 7-day sum of cases per 100k')
    st.write(chart_100k)

    st.markdown('### Daily cases since begin of the pandemic:')
    st.markdown('*Bars are stacked on top of each other.*')
    chart_cases_day = alt.Chart(df_lkr.loc[df_lkr[str_dstrct].isin(lkr_sel)])\
        .mark_bar(point=True)\
        .encode(x=alt.X('monthdate('+str_date+'):O', title='Date'),\
                y=alt.Y('mean('+str_c+'):Q', title='Cumulative Cases'),\
                color=str_dstrct,\
                tooltip=[str_dstrct,str_c])\
        .properties(width=800, height=400, title='Number of Cases')\
        .interactive()
    st.write(chart_cases_day)
