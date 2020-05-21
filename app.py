import streamlit as st
import country
import states
import landkreis
from etl import etl_main



st.title('Covid-19 Dashboard for Germany')

# run ETL pipeline
# note that the data is updated once per day, so the data pipeline is
# cached using st.cache and only needs to be rerun once per day.
df_deaths_stats, df_stats, df_cases_roll,\
        df_ctr, df_ctr_cum, df_sta, df_sta_cum,\
        df_lkr, df_lkr_cum, df_cases_loc_long\
        = etl_main()

# navigation sidebar
nav_country_map = 'Country Map'
nav_country = 'Country Data'
nav_states = 'State Data'
nav_districts = 'District Data'
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
    landkreis.main(df_lkr, df_cases_roll)
