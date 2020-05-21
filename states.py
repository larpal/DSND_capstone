import streamlit as st
import pandas as pd
import altair as alt
import data_wrangling as data
import streamlit as st
from tabulate import tabulate


def main():

    #df_ctr_cum = data.df_ctr_cum
    #df_ctr = data.df_ctr
    df_sta = data.df_sta
    df_sta_cum = data.df_sta_cum
    #df_cases = data.df_cases
    _width = data._width
    _height = data._height

    # Site Navigation
    states_tp = tuple(sorted(list(df_sta['Bundesland'].unique())))
    st.sidebar.markdown('**  Cumulative cases over time **')
    state_sel_cum = st.sidebar.selectbox('Choose State',states_tp, 0)
    st.sidebar.markdown('**  Comparison of daily cases **')
    states_sel = st.sidebar.multiselect('Choose States',states_tp, ['Bayern'])


    #
    tr_opt1,tr_opt2 = 'Line Plot', 'Stacked Bar Plot'

    toggle_radio = st.sidebar.radio('Choose style for plot',\
                            (tr_opt1,tr_opt2))

    # bar chart showing the total number of cases and deaths in every state

    st.markdown('### Distribution of cases by states:')

    df_sta_tot = df_sta.groupby('Bundesland').sum()[['AnzahlFall','AnzahlTodesfall']]\
        .sort_values(by='AnzahlFall', ascending=False).reset_index()
    df_sta_tot = df_sta_tot.melt(id_vars='Bundesland', value_vars = ['AnzahlFall', 'AnzahlTodesfall'], value_name='Cases')

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
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(Number):Q',\
                            title='Cumulative Cases',\
                            stack=None),\
                    color='category',\
                    tooltip=['monthdate(Meldedatum)','category','Number'])\
            .properties(width=800, height=400, title='Number of Cases in '+state_sel_cum)
    st.write(chart_sta_cum)
    # plot the current daily new cases as a stacked bar Plot
    # or a line plot

    st.markdown('### Daily cases since begin of the pandemic:')
    st.markdown('*(Choose states to compare and plot style in the sidebar.)*')

    if toggle_radio == tr_opt1:
        #st.markdown('Line Chart:')
        c = alt.Chart(df_sta.loc[df_sta['Bundesland'].isin(states_sel)])\
            .mark_line(point=True)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(AnzahlFall):Q', title='Cumulative Cases'),\
                    color='Bundesland',\
                    tooltip=['Bundesland','AnzahlFall'])\
            .properties(width=800, height=400, title='Reported cases per day')\
            .interactive()
        st.write(c)

    elif toggle_radio == tr_opt2:
        #st.text('Numbers stacked on top.')
        c2 = alt.Chart(df_sta.loc[df_sta['Bundesland'].isin(states_sel)])\
            .mark_bar(point=True)\
            .encode(x=alt.X('monthdate(Meldedatum):O', title='Date'),\
                    y=alt.Y('mean(AnzahlFall):Q', title='Cumulative Cases'),\
                    color='Bundesland',\
                    tooltip=['Bundesland','AnzahlFall'])\
            .properties(width=800, height=400, title='Reported cases per day')\
            .interactive()
        st.write(c2)

    #st.sidebar.markdown(\
    #    tabulate(df_cases.groupby('Bundesland').sum()[['AnzahlFall','AnzahlTodesfall']],tablefmt="pipe", headers="keys"))
    #st.write(df_cases.groupby('Bundesland').sum()[['AnzahlFall','AnzahlTodesfall']]\
    #    .sort_values(by='AnzahlFall', ascending=False).to_markdown())
    #st.write(df_cases)
