import pandas as pd
import numpy as np
import streamlit as st


# set plot properties
_width = 800
_height = 500

# read data
# qucik stats
df_stats = pd.read_csv('data_stats.csv')

def read_data_fix_date(file_name):
    df = pd.read_csv(file_name)
    df['Meldedatum'] = pd.to_datetime(df['Meldedatum'], format='%Y/%m/%d')
    return df
# country data
df_ctr = read_data_fix_date('data_ctr_long.csv')
df_ctr_cum = read_data_fix_date('data_ctr_cum_long.csv')
# state data
df_sta = read_data_fix_date('data_sta_long.csv')
"""
df_cases = read_data_fix_date('data_cases.csv')
df_deaths = read_data_fix_date('data_deaths.csv')
df_recovered = read_data_fix_date('data_recovered.csv')
df_cases_rolling = read_data_fix_date('data_cases_rolling.csv')

# Country level data
df_ctr_cum = np.cumsum(df_cases.groupby(['Meldedatum'])\
                            .sum()[['AnzahlFall','AnzahlGenesen','AnzahlTodesfall']])
df_ctr_cum = df_ctr_cum.reset_index()
df_ctr_cum = \
            pd.melt(df_ctr_cum.reset_index(), id_vars=['Meldedatum'],\
            value_vars = ['AnzahlFall','AnzahlGenesen','AnzahlTodesfall'],\
            var_name = 'category',\
            value_name = 'Number')

df_ctr_tmp = df_cases.groupby(['Meldedatum'])\
                        .sum()[['AnzahlFall','AnzahlTodesfall']]
df_ctr = \
        pd.melt(df_ctr_tmp.reset_index(), id_vars=['Meldedatum'],\
                value_vars = ['AnzahlFall','AnzahlTodesfall'],\
                var_name = 'category',\
                value_name = 'Number')


# State level data
df_sta = df_cases.groupby(['Meldedatum','Bundesland']).sum().reset_index()\
                [['Meldedatum','Bundesland','AnzahlFall','AnzahlTodesfall']]
# District level
df_lkr = df_cases.groupby(['Meldedatum','Landkreis']).sum().reset_index()\
                [['Meldedatum','Landkreis','AnzahlFall','AnzahlTodesfall']]

df_lkr_roll = \
        pd.melt(df_cases_rolling, id_vars=['Meldedatum', 'Landkreis'],\
                value_vars = ['AnzahlFall100k'],\
                var_name = 'category',\
                value_name = 'Number')
"""
