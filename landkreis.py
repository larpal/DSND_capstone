import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data
import streamlit as st

def main():

    df_ctr_cum = data.df_ctr_cum
    df_ctr = data.df_ctr
    df_sta = data.df_sta
    df_lkr = data.df_lkr
    df_lkr_roll = data.df_lkr_roll
    _width = data._width
    _height = data._height

    lkr_tp = tuple(sorted(list(df_lkr['Landkreis'].unique())))
    print(lkr_tp)
    lkr_sel = st.sidebar.multiselect('Choose Districts',lkr_tp,['SK Hamburg'])

    st.write('Total Cases')
    c = alt.Chart(df_lkr.loc[df_lkr['Landkreis'].isin(lkr_sel)])\
        .mark_bar(point=True)\
        .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                y=alt.Y('mean(AnzahlFall):Q', title='Cumulative Cases'),\
                color='Landkreis',\
                tooltip=['Landkreis','AnzahlFall'])\
        .properties(width=800, height=400, title='Number of Cases')\
        .interactive()
    st.write(c)

    line_data = pd.DataFrame({'a': [50]})
    c3 = alt.Chart(line_data).mark_rule(strokeWidth=10).encode(y='a:Q',\
                                            opacity=alt.value(0.2),
                                            color = alt.value('red'))
    c2 = alt.Chart(df_lkr_roll.loc[df_lkr_roll['Landkreis'].isin(lkr_sel)])\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q', title='Cases'),\
                    color='Landkreis',\
                   tooltip = ['Landkreis','Meldedatum','Number'])
    c4 = (c2+c3).properties(width=800, height=400, title='Rolling 7-day sum of cases per 100k')
    st.write(c4)
