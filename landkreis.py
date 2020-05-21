import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data
import streamlit as st
import numpy as np

str_c = data.str_c
str_d = data.str_d
str_r = data.str_r
str_dstrct = data.str_dstrct

def main(df_lkr, df_cases_rolling, df_loc):

    # get plot properties
    _width = data._width
    _height = data._height

    df_lkr_roll = \
            pd.melt(df_cases_rolling, id_vars=['Meldedatum', str_dstrct],\
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
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(cases):Q', title='Cases'),\
                    color=str_dstrct,\
                   tooltip = [str_dstrct,'Meldedatum','cases'])
    chart_100k = (chart_cases_per_100k+chart_line).properties\
    (width=800, height=400, title='Rolling 7-day sum of cases per 100k')
    st.write(chart_100k)

    st.markdown('### Daily cases since begin of the pandemic:')
    st.markdown('*Bars are stacked on top of each other.*')
    c = alt.Chart(df_lkr.loc[df_lkr[str_dstrct].isin(lkr_sel)])\
        .mark_bar(point=True)\
        .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                y=alt.Y('mean('+str_c+'):Q', title='Cumulative Cases'),\
                color=str_dstrct,\
                tooltip=[str_dstrct,str_c])\
        .properties(width=800, height=400, title='Number of Cases')\
        .interactive()
    st.write(c)
    #st.write(df_loc[['lat','lon']].head(1000))
    #st.map(df_loc[['lat','lon']].head(10000))
