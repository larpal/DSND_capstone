import pandas as pd
import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression

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

def predict_days(df, n_training, n_ahead, class_to_predict,str_date='date_reported'):
    """Predict the number of Covid cases/deaths/recoverd via Linear regression

    df (pandas data frame): data frame containing past Covid data
    n_training (int): number of recent days used to train linear regression
    n_ahead (int): number of days to predict ahead
    class_to_predict (str): string indicating whether to predict cases, deaths,
    or recovered
    """
    # create training samples
    X = pd.to_numeric(\
            pd.to_datetime(df.loc[df['category']==class_to_predict].iloc[-n_training:][str_date],\
                            format='%Y/%m/%d'))
    X = X.to_numpy().reshape(-1,1)

    # create training ground truth
    y = df.loc[df['category']==class_to_predict].iloc[-n_training:]['Number']
    y = y.to_numpy().reshape(-1,1)
    # fit linear regression based on log of y
    lr = LinearRegression()
    lr.fit(X,np.log(y))
    # dates to predict
    dates_to_predict = pd.Series([pd.Timestamp.today()\
                        + pd.DateOffset(idx) for idx in \
                                  list(np.linspace(1,n_ahead,n_ahead).astype(int))]).dt.normalize()
    #print(dates_to_predict)
    predictions = np.exp(lr.predict(pd.to_numeric(pd.Series(dates_to_predict))\
           .to_numpy().reshape(-1,1)\
          ))
    df_predicted = pd.DataFrame({'date':dates_to_predict, \
                         'predictions':pd.Series(predictions.reshape(-1))})
    df_predicted['category'] = class_to_predict
    df_predicted['predictions'] =  df_predicted['predictions'].apply(np.round).astype(int)
    return df_predicted
