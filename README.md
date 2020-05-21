# DSND_capstone

##### Table of Contents
* [Project Overview](#project-overview)
* [Data Sources](#data-sources)
* [Libraries](#libraries)
* [Code Structure and Usage](#Code-Structure-and-Usage)

## Project Overview
In this project, I created a dashboard displaying relevant information about
the Covid-19 pandemic in Germany. The main goals of the project were:
- Find relevant data sources for Covid-19 data in Germany
- Combine data sources to provide information about the geographic distribution of Covid-19 cases
- Present the information in a useful and pretty way.


My dashboard consists of four pages containing several different types of visualizations:
- Country level information:
  * Table with stats for current day
  * Bar chart showing age distribution of deaths
  * Cumulative plot of all reported cases/deaths/recovered
  * Bar chart showing daily cases/deaths/recovered since begin of the pandemic
- A map of Germany overlayed by a heatmap indicating the total or last week's number of cases per 100.000 inhabitants for each district
- State level information:
  * Bar chart of total cases and deaths by state
  * Cumulative plot of all reported cases/deaths/recovered for a chosen state
  * Line or stacked bar chart showing daily cases/deaths/recovered since begin of the pandemic for a number of chosen states
- District level information:
  * Line chart showing rolling sum of the past 7 days' cases per 100k
    inhabitants
  * Stacked bar plot showing the daily number of reported cases

This project was done within the framework of the [Data Science Nanodegree](#https://www.udacity.com/course/data-scientist-nanodegree--nd025) program offered by Udacity.
## Data Sources
The main data source for the dashboard is the Covid-19 data ([link](#https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74)) provided by the
Robert-Koch-Institute. The data set includes information about each Covid-19
case officially reported in Germany, such as:
* date of reporting
* case ID
* information about whether the individual is infected / recovered / dead
* state
* district name and ID
* sex of infected person
* age (six different groups)

In addition, I used a data set from *DESTATIS* [(link)](#https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.html) with information
about each district in Germany, such as
* district ID
* district name
* number of inhabitants

I used this data in order to normalize the number of Covid-19 cases with
respect to the number of inhabitants in each district. Currently, an important
figure to decided about social distancing measures is the number of infections
per 100.000 people per week. I combined the above to data sets to compute these
metrics.

Last, I used [this](#https://public.opendatasoft.com/explore/dataset/landkreise-in-germany/export/)
data set containing location data for all districts in Germany. From this
data set, I pulled the coordinates of each district in Germany to show
the number of cases per 100k inhabitants on a map.

## Libraries
The dashboard is built using the following libraries:
- [Streamlit](#https://www.streamlit.io): to run the app, use `streamlit run app.py`
- [Pandas](#https://pandas.pydata.org)
- [Numpy](#https://numpy.org)
- [xlrd](#https://xlrd.readthedocs.io/en/latest/): while this is not imported implicitely, it needs to be installed to read an `xlsx` file using `pd.read_excel`.
- [Altair](#https://altair-viz.github.io): all charts (except for the geographic map) displayed in the dashboard are built using Altair.


## Code Structure and Usage
```

|-- data
|   |-- 04-kreise.xlsx
|   |-- landkreise-in-germany.csv
|-- app.py              # main file to run app
|-- country.py          # functions to create country level visualizations
|-- data_wrangling.py   # helper functions
|-- etl.py              # ETL pipeline
|-- landkreis.py        # functions to create district level visualizations
|-- states.py           # functions to create state level visualizations
```

To run the app, simply use `streamlit run app.py`. Note that the ETL pipeline is run once when the app is started which may take a few minutes. The data is then cached inside the app (using `st.cache`) and only needs to be updated once per day.


## Data Processing
The data preprocessing is done in the `etl` module via the `etl_main` function. The code contained can be explored in an easier way using the notebook `ETL.ipynb` which contains the same code broken into smaller pieces.



## Future Work
There are I am planning to improve, such as:
- deploy the app on Heroku
- Add more interactive information to the map
