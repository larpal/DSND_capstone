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



st.title('COVID-19 Dashboard for Germany')

# run ETL pipeline
# note that the data is updated once per day, so the data pipeline is
# cached using st.cache and only needs to be rerun once per day.
df_deaths_stats, df_stats, df_cases_roll,\
        df_ctr, df_ctr_cum, df_sta, df_sta_cum,\
        df_lkr, df_lkr_cum, df_cases_loc_long\
        = etl_main()

# navigation sidebar
nav_country_map = 'Country Map'
nav_country = 'Country Stats'
nav_states = 'States'
nav_districts = 'Districts'
site_navigation = \
    st.sidebar.radio('Site Navigation',\
                            (nav_country,nav_country_map,nav_states,nav_districts))

# run chosen subpage
if site_navigation == nav_country:
    country.main(df_stats, df_deaths_stats, df_ctr, df_ctr_cum)
elif site_navigation == nav_country_map:
    country.show_map(df_cases_loc_long)
elif site_navigation == nav_states:
    states.main(df_sta, df_sta_cum)
elif site_navigation == nav_districts:
    landkreis.main(df_lkr, df_cases_roll, df_cases_loc_long)
