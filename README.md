# DSND_capstone

##### Table of Contents
* [Project Overview](#project-overview)
* [Project Design](#project-design)
* [Data Sources](#data-sources)
* [Data Processing](#data-processing)
* [Analysis](#analysis)
* [Visualizations and Web App](#visualizations-and-web-app)
* [Notes about the Code](#notes-about-the-code)
* [Conclusion](#conclusion)

## Project Overview

This project was done within the framework of the [Data Science Nanodegree](https://www.udacity.com/course/data-scientist-nanodegree--nd025) program offered by Udacity. This readme serves both as a project description and as information on how to use the code.

In this project, I created a dashboard displaying relevant information about
the Covid-19 pandemic in Germany. The app is deployed on Heroku and an be accessed [here](https://pacific-savannah-97681.herokuapp.com).
My personal goal was to create a dashboard that my family members can use in order to get a reasonable overview about the current state
of the pandemic both in the whole country but also within their area. Thus, I tried to create a dashboard that is pretty and easy to understand but still presents quite a large amount of information.


The main work packages of the project were:
- **Project design:** define the types of information to be visualized and the structure of the web app
- **Data gathering:** find relevant data sources for Covid-19 data in Germany as well as background information about districts and states.
- **Data processing:** filter out the relevant information from the data sources and combine the data
- **Analysis:** use processed data to compute the relevant statistics to be displayed and implement a linear regression to predict future cases
- **Visualizations:** Build beautiful charts to visualize the information
- **Software Engineering:** Refactor code into packages and build a web app

Each step of the project will be explained in more detail in the following.


## Project Design

I chose the following statistics to be displayed in my app:

- Number of total cases over time on a country, state and district level. These numbers give a high level overview about the severity of the pandemic
- Number of daily cases and in particular how this changes over time. These numbers are more informative since it is easier to see the current number of new cases per day and compare it with, e.g., the peak of the pandemic.
- Number of cases per 100.000 inhabitants in a 7 day time window. This is likely the most informative figure as it is normalized by population. It is currently one of the main metrics to decide about relaxing or tightening social distancing measures or similar restrictions.

To structure the dashboard, I created four pages containing several different types of visualizations:
- **Country Data:**
  * Table with stats for current day
  * Bar chart showing age distribution of deaths
  * Cumulative plot of all reported cases/deaths/recovered
  * Bar chart showing daily cases/deaths/recovered since begin of the pandemic
- **Country Map:** A map of Germany overlayed by a heatmap indicating the total or last week's number of cases per 100.000 inhabitants for each district
- **State Data**:
  * Bar chart of total cases and deaths by state
  * Cumulative plot of all reported cases/deaths/recovered for a chosen state
  * Line or stacked bar chart showing daily cases/deaths/recovered since begin of the pandemic for a number of chosen states
- **District Data**:
  * Line chart showing rolling sum of the past 7 days' cases per 100k
    inhabitants
  * Stacked bar plot showing the daily number of reported cases


## Data Sources
The main data source for the dashboard is the Covid-19 data ([link](https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74)) provided by the
Robert-Koch-Institute (RKI). The data set includes information about each Covid-19
case officially reported in Germany, such as:
* date of reporting
* case ID
* information about whether the individual is infected / recovered / dead
* state
* district name and ID
* sex of infected person
* age (six different groups)

In addition, I used a data set from *DESTATIS* [(link)](https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.html) with information
about each district in Germany, such as
* district ID
* district name
* number of inhabitants

I used this data in order to normalize the number of Covid-19 cases with
respect to the number of inhabitants in each district. Currently, an important
figure to decided about social distancing measures is the number of infections
per 100.000 people per week. I combined the above to data sets to compute these
metrics.

Last, I used [this](https://public.opendatasoft.com/explore/dataset/landkreise-in-germany/export/)
data set containing location data for all districts in Germany. From this
data set, I pulled the coordinates of each district in Germany to show
the number of cases per 100k inhabitants on a map.

## Data Processing
The data preprocessing is done in the `etl` module via the `etl_main` function. The code contained can be explored in an easier way using the notebook `ETL.ipynb` which contains the same code broken into smaller pieces.
The main steps of the process are:

* Download current data from RKI webpage
* Clean data according to RKI information to compute daily reported cases/recovered/deaths
* Remove irrelevant columns
* Get population data, clean it in order to match the district names of RKI data
* Combine RKI data with population data to compute cases normalized by population
* Compute 7 day rolling averages
* Transform all relevant data into long data format for visualization with Altair

## Analysis
All relevant statistics used for visualization are straightforward to compute. While this project focuses more on the software engineering and presentations sides of data science, I added a linear regression model to predict the numbers for cases/deaths/recovered for next three days. In particular, I am using the model to predict the logarithm of these numbers. The rationale is that the spread of the virus is (on a large scale) naturally an exponential process.

## Visualizations and Web App
The web app is built using [streamlit](https://www.streamlit.io) as its core infrastructure. The visualizations are done using [Altair](https://altair-viz.github.io) and the map is created with [pydeck](https://pypi.org/project/pydeck/) and its streamlit plugin.


## Notes about the Code
### Libraries
The dashboard is built using the following libraries:
- [Altair](https://altair-viz.github.io): all charts (except for the geographic map) displayed in the dashboard are built using Altair.
- [Numpy](https://numpy.org)
- [Pandas](https://pandas.pydata.org)
- [Pydeck](https://pypi.org/project/pydeck/)
- [Scikit-Learn](https://scikit-learn.org/stable/)
- [Streamlit](https://www.streamlit.io): provides the main infrastructure of the app
- [xlrd](https://xlrd.readthedocs.io/en/latest/): while this is not imported implicitely, it needs to be installed to read an `xlsx` file using `pd.read_excel`.



### Code Structure and Usage
```

|-- data
|   |-- 04-kreise.xlsx  # population data
|   |-- landkreise-in-germany.csv  # location data
|-- app.py              # main file to run app
|-- country.py          # functions to create country level visualizations
|-- data_wrangling.py   # helper functions
|-- etl.py              # ETL pipeline
|-- landkreis.py        # functions to create district level visualizations
|-- states.py           # functions to create state level visualizations
```

To run the app, simply use `streamlit run app.py`. Note that the ETL pipeline is run once when the app is started which may take a few minutes. The data is then cached inside the app (using `st.cache`) and only needs to be updated once per day or when the app is restarted.




## Conclusion
In this project, I created a dashboard to visualize the current Covid-19 situation in Germany. For this purpose, I gathered data from different sources, cleaned and combined the data, computed relevant statistics and predictions and presented the results via many different visualizations in a web application.
I found that Streamlit is very well suited for such dashboards. In particular, I think that this is a great tool to build pretty dashboards very quickly. Further, I feel that Altair is a great tool to create beautiful and interactive charts.

Once the time allows, there are I am planning to improve, such as:
- ~Deploy the app on Heroku.~ *(Update June 14: deployed [here](https://pacific-savannah-97681.herokuapp.com))*
- Add more interactive information to the map. I was impressed by how easy it is to add a map and overlay it with data. Next, I would like to add the relevant information such as district and cases that is displayed when hovering over a hexagon.
- Speed up the ETL pipeline: the pipeline currently takes a few minutes to run which has to be performed once per day when the new data is added. I am confident that this can be sped up significantly.
- refactor the ETL pipeline into pieces that are easier to digest


## Licensing, Authors, and Acknowledgements
I am grateful to the providers of the data sets mentioned above.
