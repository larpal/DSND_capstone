import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import country
import states
import landkreis
import data_wrangling
from tabulate import tabulate
from etl import etl_main


#data_wrangling.init()

#data_wrangling.df_ctr_cum
#
st.title('COVID-19 Dashboard for Germany')

df_deaths_stats, df_stats, df_cases_roll,\
        df_ctr, df_ctr_cum, df_sta, df_sta_cum,\
        df_lkr, df_lkr_cum, df_cases_loc_long\
        = etl_main()


nav_country_map = 'Country Map'
nav_country = 'Country Stats'
nav_states = 'States'
nav_districts = 'Districts'
site_navigation = \
    st.sidebar.radio('Site Navigation',\
                            (nav_country,nav_country_map,nav_states,nav_districts))

if site_navigation == nav_country:
    #country_main(df_ctr_cum,df_ctr,_width,_height)
    country.main(df_stats, df_deaths_stats, df_ctr, df_ctr_cum)
elif site_navigation == nav_country_map:
    country.show_map(df_cases_loc_long)
elif site_navigation == nav_states:
    states.main(df_sta, df_sta_cum)
elif site_navigation == nav_districts:
    landkreis.main(df_lkr, df_cases_roll, df_cases_loc_long)
    pass
#
