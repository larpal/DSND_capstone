import pandas as pd
import numpy as np
import streamlit as st
import data_wrangling as data

str_c = data.str_c
str_d = data.str_d
str_r = data.str_r

@st.cache
def etl_main():
    # get Covid data from RKI webpage
    df_rki = pd.read_csv('https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data')
    df_rki['Meldedatum'] = pd.to_datetime(df_rki['Meldedatum'], format='%Y/%m/%d')

    df_rki.rename(columns={'AnzahlFall': str_c,\
                            'AnzahlTodesfall':str_d,\
                            'AnzahlGenesen':str_r},\
                            inplace = True)
    st.write(df_rki)
    # compute basic stats
    n_cases = df_rki.loc[df_rki['NeuerFall'].isin([0,1])][str_c].sum()
    n_cases_new = \
        df_rki.loc[df_rki['NeuerFall'].isin([-1,1])][str_c].sum()
    n_deaths = \
     df_rki.loc[df_rki['NeuerTodesfall'].isin([0,1])][str_d].sum()
    n_deaths_new = \
     df_rki.loc[df_rki['NeuerTodesfall'].isin([-1,1])][str_d].sum()
    n_recovered = \
        df_rki.loc[df_rki['NeuGenesen'].isin([0,1])][str_r].sum()
    n_recovered_new = \
        df_rki.loc[df_rki['NeuGenesen'].isin([-1,1])][str_r].sum()
    n_active = n_cases - n_deaths - n_recovered
    n_active_new = n_cases_new - n_deaths_new - n_recovered_new

    df_stats = pd.DataFrame({' ':['Total','Today'],\
                        'Cases':[n_cases, n_cases_new],\
                        'Recovered':[n_recovered, n_recovered_new],\
                        'Deaths':[n_deaths, n_deaths_new],\
                        'Unresolved':[n_active, n_active_new]})
    df_stats.set_index(' ', inplace=True)

    # separate cases, deaths and recovered cases
    df_cases = df_rki.loc[df_rki['NeuerFall'].isin([0,1])].copy()
    df_deaths = df_rki.loc[df_rki['NeuerTodesfall'].isin([0,1])].copy()
    df_recovered = df_rki.loc[df_rki['NeuGenesen'].isin([0,1])].copy()

    df_deaths_stats = pd.get_dummies(df_deaths['Altersgruppe']).sum().reset_index()
    df_deaths_stats.rename(columns={'index':'Age',0:'Count'}, inplace=True)

    # drop unnecessary columns
    df_cases.drop(columns=\
        [str_d,'NeuerTodesfall',str_r,\
         'NeuGenesen','Altersgruppe2'],\
          inplace=True)
    df_deaths.drop(columns=\
        [str_c,'NeuerFall','NeuGenesen',\
         str_r,'Altersgruppe2'], \
         inplace=True)
    df_recovered.drop(columns=\
        [str_c,'NeuerFall',str_d,\
         'NeuerTodesfall','Altersgruppe2'], \
         inplace=True)

    # merge Berlin cases since we currently don't have population data for the individual districts
    df_cases.loc[df_cases['IdLandkreis'].isin(np.arange(11000,11013,1)),'IdLandkreis'] = 11000
    df_cases.loc[df_cases['IdLandkreis'].isin(np.arange(11000,11013,1)),'Landkreis'] = 'SK Berlin'
    df_cases.drop(columns = ['Datenstand'], inplace=True)

    # one-hot encode age groups
    df_cases = pd.concat([df_cases,pd.get_dummies(df_cases['Altersgruppe'], prefix='age')],axis=1).drop(columns='Altersgruppe')
    df_cases.head()

    # needs packae xlrd
    df_population = pd.read_excel('./data/04-kreise.xlsx', \
        sheet_name='Kreisfreie Städte u. Landkreise',skiprows=6, skipfooter=16)
    df_population.columns = \
        ['IdLandkreis', 'Bezeichnung','Name','NUTS3',\
         'area','pop_tot','pop_male','pop_female','pop_per_sqkm2']
    df_population.dropna(axis=0, how='any', inplace=True)
    # set integer IdLandkreis
    df_population['IdLandkreis'] = df_population['IdLandkreis'].astype(int)

    # create data frame  with cases per 100k inhabitants in the last 7 days
    df_to_roll = df_cases.copy()[['Meldedatum',str_c,'IdLandkreis']].\
        groupby(['Meldedatum','IdLandkreis']).sum().reset_index()
    df_to_roll.sort_values(by='Meldedatum',inplace = True)

    # pad zero rows for days on which no new cases were reported
    lkr_all = set(df_to_roll['IdLandkreis'].unique())
    # sweep over all days in the data set
    for date in pd.date_range(df_to_roll['Meldedatum'].min(), \
                                df_to_roll['Meldedatum'].max(), freq = '1D'):
        # add zero rows for all districts that didn't report cases on that day
        for id_lkr in lkr_all - \
            set(df_to_roll.loc[df_to_roll['Meldedatum'] == date ]['IdLandkreis']):
            df_to_roll = \
                df_to_roll.append({'Meldedatum':date, \
                                   'IdLandkreis': id_lkr,\
                                   str_c:0}, \
                                   ignore_index=True)
        print('fixed date',date)

    df_to_roll.sort_values(by='Meldedatum',inplace = True)
    df_to_roll = df_to_roll.set_index('Meldedatum').\
                    groupby('IdLandkreis').rolling('7d').sum()
    df_to_roll = df_to_roll.drop(columns = ['IdLandkreis']).reset_index()

    df_cases_roll = pd.merge(df_to_roll, df_population,on='IdLandkreis')
    df_cases_roll.insert(3,'AnzahlFall100k',0)
    df_cases_roll['AnzahlFall100k'] = \
        df_cases_roll[str_c]/df_cases_roll['pop_tot']*(10**5)
    df_cases_roll.loc[df_cases_roll['IdLandkreis']==5558].tail(25)

    # set district ids to district names
    df_cases_roll['Landkreis'] = df_cases_roll['IdLandkreis']
    # make sure that the district name matches the original one from the cases
    # data frame
    # (this step is a bit slow, could likely be improved)
    df_cases_roll['Landkreis'] = \
     df_cases_roll['Landkreis'].apply(lambda x: \
        df_cases.loc[df_cases['IdLandkreis'] == x]['Landkreis'].iloc[0])
    df_cases_roll.rename(columns=\
        {"AnzahlFall":"7d_AnzahlFall",'AnzahlFall100k':'7d_AnzahlFall100k'})

    """
    Transform data to long data format for better plotting using Altair
    """
    # Country
    df_ctr_cases = df_cases.groupby(['Meldedatum'])\
                            .sum()[[str_c]]
    df_ctr_deaths = df_deaths.groupby(['Meldedatum'])\
                            .sum()[[str_d]]
    df_ctr_recovered = df_recovered.groupby(['Meldedatum'])\
                            .sum()[[str_r]]
    df_ctr_cases = pd.melt(df_ctr_cases.reset_index(), id_vars=['Meldedatum'],\
                                                       value_vars = [str_c],\
                                                       var_name = 'category',\
                                                       value_name = 'Number')
    df_ctr_deaths = pd.melt(df_ctr_deaths.reset_index(), id_vars=['Meldedatum'],\
                                                       value_vars = [str_d],\
                                                       var_name = 'category',\
                                                       value_name = 'Number')
    df_ctr_recovered = pd.melt(df_ctr_recovered.reset_index(), id_vars=['Meldedatum'],\
                                                       value_vars = [str_r],\
                                                       var_name = 'category',\
                                                       value_name = 'Number')
    df_ctr = pd.concat([df_ctr_cases,df_ctr_deaths,df_ctr_recovered], axis = 0)
    df_ctr['category'] = df_ctr['category']\
            .apply(lambda x: 'case' if x == str_c else\
                                  ('death' if x == str_d else 'recovered'))
    # cumulative cases
    df_ctr_cum = df_ctr.copy().sort_values(by=['Meldedatum','category'])
    for el in list(df_ctr_cum['category'].unique()):
        df_ctr_cum.loc[df_ctr_cum['category']== el,'Number' ] = \
            np.cumsum(df_ctr_cum.loc[df_ctr_cum['category']== el,'Number' ])
    """States"""
    # daily cases
    df_sta = pd.concat([df_cases.groupby(['Meldedatum','Bundesland']).sum().reset_index()\
                    [['Meldedatum','Bundesland',str_c]],\
                df_deaths.groupby(['Meldedatum','Bundesland']).sum().reset_index()\
                                [['Meldedatum','Bundesland',str_d]],\
                df_recovered.groupby(['Meldedatum','Bundesland']).sum().reset_index()\
                                [['Meldedatum','Bundesland',str_r]]])
    df_sta = df_sta.fillna(0).groupby(['Meldedatum','Bundesland']).sum().reset_index()
    df_sta[[str_c,str_d,str_r]] = df_sta[[str_c,str_d,str_r]].astype('int64')

    # cumulative
    df_sta_cum = df_sta.copy()
    for state in list(df_sta['Bundesland'].unique()):
        for col in [str_c,str_d,str_r]:
            df_sta_cum.loc[df_sta_cum['Bundesland']==state,col] = \
            np.cumsum(df_sta_cum.loc[df_sta_cum['Bundesland']==state,col])
    """Districts"""
    df_lkr = pd.concat([df_cases.groupby(['Meldedatum','Landkreis']).sum().\
            reset_index()[['Meldedatum','Landkreis',str_c]],\
        df_deaths.groupby(['Meldedatum','Landkreis']).sum().\
            reset_index()[['Meldedatum','Landkreis',str_d]],\
        df_recovered.groupby(['Meldedatum','Landkreis']).sum().\
            reset_index()[['Meldedatum','Landkreis',str_r]]])
    df_lkr = df_lkr.fillna(0).groupby(['Meldedatum','Landkreis']).sum().reset_index()
    df_lkr[[str_c,str_d,str_r]] = df_lkr[[str_c,str_d,str_r]].astype('int64')

    df_lkr_cum = df_lkr.copy()
    for el in list(df_lkr['Landkreis'].unique()):
        for col in [str_c,str_d,str_r]:
            df_lkr_cum.loc[df_lkr_cum['Landkreis']==el,col] = np.cumsum(df_lkr_cum.loc[df_lkr_cum['Landkreis']==el,col])
    df_lkr_cum

    """
    Location Data: Merge reported cases with the location of the district so that
    we can plot a heatmap of the number of cases on an actual map of Germany.
    Data set is taken from
    https://public.opendatasoft.com/explore/dataset/landkreise-in-germany/export/
    """
    #geo_data = pd.read_csv('https://public.opendatasoft.com/explore/dataset/landkreise-in-germany/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B')
    geo_data = pd.read_csv('./data/landkreise-in-germany.csv', delimiter = ';',\
                           usecols=['Geo Point','Name 2','Cca 2', 'Type 2'])
    # drop NaN row corresponding to a lake
    geo_data.dropna(axis=0, inplace = True)
    geo_data[['lat','lon']] = geo_data['Geo Point'].str.split(',', expand=True)
    geo_data.drop(columns = 'Geo Point',inplace = True)
    geo_data.rename(columns = \
        {'Name 2':'Name','Cca 2':'IdLandkreis','Type 2':'Type of District'}, \
        inplace =True)
    df_cases_loc = pd.merge(df_cases, geo_data, \
            on='IdLandkreis')\
            [['IdLandkreis','Meldedatum',str_c,'lat','lon']]
    # normalize to cases per 100k inhabitants
    df_cases_loc = pd.merge(df_cases_loc,df_population[['IdLandkreis','pop_tot']],on='IdLandkreis')
    df_cases_loc[str_c] = df_cases_loc[str_c]/df_cases_loc['pop_tot']*10**5
    df_cases_loc[str_c] = df_cases_loc[str_c].apply(np.round).astype(int)
    #
    """
    When plotting the map, we only use the geological coordinates of the reported
    case. Currently, each row contains information about how many cases were
    reported. Thus, we create a new row for every reported cases and copy the
    coordinates of the district.
    """
    df_cases_loc_long = df_cases_loc.loc[df_cases_loc[str_c] == 1]
    for n_cases in sorted(df_cases_loc[str_c].unique())[1:]:
        for k in range(n_cases):
            df_cases_loc_long = \
                pd.concat([df_cases_loc_long, df_cases_loc.loc[df_cases_loc[str_c] == n_cases]])
    df_cases_loc_long.drop(columns=str_c, inplace = True)

    # data frame with only past week's cases
    df_cases_7d = df_cases_loc_long.loc[(pd.Timestamp.today() - \
                                    df_cases_loc_long['Meldedatum']).dt.days < 7]
    """
    # save data
    df_deaths_stats.to_csv('data_death_stats.csv', index=False)
    df_stats.to_csv('data_stats.csv')
    df_cases_roll.to_csv('data_cases_rolling.csv', index=False)
    # country data
    df_ctr.to_csv('data_ctr_long.csv', index=False)
    df_ctr_cum.to_csv('data_ctr_cum_long.csv', index=False)
    # state data
    df_sta.to_csv('data_sta_long.csv', index=False)
    df_sta_cum.to_csv('data_sta_cum_long.csv', index=False)
    # district data
    df_lkr.to_csv('data_lkr_long.csv', index=False)
    df_lkr_cum.to_csv('data_lkr_cum_long.csv', index=False)
    # location case data
    df_cases_loc_long.to_csv('data_loc_long.csv', index=False)
    """
    return df_deaths_stats, df_stats, df_cases_roll,\
            df_ctr, df_ctr_cum, df_sta, df_sta_cum,\
            df_lkr, df_lkr_cum, df_cases_loc_long
