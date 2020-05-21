import pandas as pd
import numpy as np
import streamlit as st


# set plot properties
_width = 800
_height = 500
# set naming properties
str_c = 'cases'
str_d = 'deaths'
str_r = 'recovered'
str_dstrct = 'district'
str_date = 'date_reported'


def longify_df_cum(df_cum,cat,sel):
    """ transform data frame with cumulative data for states or districts
        into long format for a specific state/district.

        Args:
        df_cum: either df_sta_cum or df_lkr_cum
        cat (str): 'Bundesland' or 'Landkreis'
        sel (str): specific Bundesland or Landkreis
    """
    tmp = df_cum.loc[df_cum[cat]==sel].drop(columns=[cat])
    tmp = pd.melt(tmp, id_vars = [str_date], var_name= 'category',\
        value_vars = [str_c,str_d,str_r],\
       value_name = 'Number')
    return tmp
