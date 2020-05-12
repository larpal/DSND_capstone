import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import country
import states
import landkreis
import data_wrangling
from tabulate import tabulate


#data_wrangling.init()

#data_wrangling.df_ctr_cum
#
st.title('COVID 19 Dashboard for Germany')





nav_country = 'Country Overview'
nav_states = 'States'
nav_districts = 'Districts'
site_navigation = \
    st.sidebar.radio('Site Navigation',\
                            (nav_country,nav_states,nav_districts))

if site_navigation == nav_country:
    #country_main(df_ctr_cum,df_ctr,_width,_height)
    country.main()
elif site_navigation == nav_states:
    states.main()
elif site_navigation == nav_districts:
    #landkreis.main()
    pass
#
