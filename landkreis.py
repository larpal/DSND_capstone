import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data
import streamlit as st
import numpy as np

def main():
    st.markdown('*Choose any number of districts in the sidebar.*')
    """
    df_ctr_cum = data.df_ctr_cum
    df_ctr = data.df_ctr
    df_sta = data.df_sta
    """
    df_lkr_roll = data.df_lkr_roll
    df_lkr = data.df_lkr

    df_loc = data.df_cases_loc_long

    _width = data._width
    _height = data._height

    lkr_tp = tuple(sorted(list(df_lkr['Landkreis'].unique())))
    lkr_sel = st.sidebar.multiselect('Choose Districts',lkr_tp,['SK Hamburg'])

    # chart displaying rolling sum of cases in the past week
    st.markdown('### Rolling sum of cases over past 7 days:')
    line_data = pd.DataFrame({'a': [50]})
    # line at 50 cases
    chart_line = alt.Chart(line_data).mark_rule(strokeWidth=10).encode(y='a:Q',\
                                            opacity=alt.value(0.2),
                                            color = alt.value('red'))
    chart_cases_per_100k = \
    alt.Chart(df_lkr_roll.loc[df_lkr_roll['Landkreis'].isin(lkr_sel)])\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', title='Cases'),\
                    color='Landkreis',\
                   tooltip = ['Landkreis','Meldedatum','Number'])
    chart_100k = (chart_cases_per_100k+chart_line).properties\
    (width=800, height=400, title='Rolling 7-day sum of cases per 100k')
    st.write(chart_100k)

    st.markdown('### Daily cases since begin of the pandemic:')

    c = alt.Chart(df_lkr.loc[df_lkr['Landkreis'].isin(lkr_sel)])\
        .mark_bar(point=True)\
        .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                y=alt.Y('mean(AnzahlFall):Q', title='Cumulative Cases'),\
                color='Landkreis',\
                tooltip=['Landkreis','AnzahlFall'])\
        .properties(width=800, height=400, title='Number of Cases')\
        .interactive()
    st.write(c)
    #st.write(df_loc[['lat','lon']].head(1000))
    #st.map(df_loc[['lat','lon']].head(10000))
