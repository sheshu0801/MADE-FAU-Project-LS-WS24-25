##Analyzing the Correlation Between Unemployment Rates and Crime Incidents in the USA (2004-2014)

## Title
<!-- Give your project a short title. -->
Analyzing the Correlation Between Unemployment Rates and Crime Incidents in the USA (2004-2014)
## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. Is there a correlation between unemployment rates and crime incidents in the USA from 2004 to 2014?
2. Which states exhibit the highest correlation between unemployment rates and crime incidents?
3. Are there specific periods within these years that show significant changes in unemployment or crime rates?
4. How do the trends in unemployment rates and crime incidents change over the years from 2004 to 2014?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->

The project investigates the relationship between unemployment rates and crime incidents in different states in the USA from 2004 to 2014. Using Kaggle datasets, it aims to uncover patterns and correlations that provide insights into socioeconomic factors affecting crime rates. The objective is to determine if there is a significant correlation between unemployment rates and crime incidents. Additionally, the project identifies states with high correlations, temporal changes, and overall trends. The methodology includes downloading and cleaning datasets, converting month data to a consistent format, filtering data for 2004 to 2014, merging unemployment and crime data, calculating incident sums for each state and year, and performing statistical analysis to measure correlations. The project will pinpoint periods and states with high variations in unemployment and crime rates. Graphical representations will illustrate the findings, and a comprehensive report will compile actionable insights. Understanding the linkage between unemployment and crime can drive policy actions for economic and social programs to help mitigate crime. This project provides valuable insights for researchers, policymakers, and social scientists.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource 1: Unemployment in America, Per US State
 
* Metadata URL: https://www.kaggle.com/datasets/justin2028/unemployment-in-america-per-us-state
* Data URL: path = kagglehub.dataset_download("justin2028/unemployment-in-america-per-us-state")
* Data Type: CSV

This is a dataset that tracks relevant population statistics and employment rates per US state since 1976.

All data are official figures from the Bureau of Labor Statistics that have been compiled and structured by myself. Besides the 50 US states, the unemployment data of three other areas are also being tracked in order to increase the analytical potential of the dataset: the District of Columbia, the Los Angeles-Long Beach-Glendale metropolitan division, and New York City.

### Datasource 2: US Crime DataSet

* Metadata URL: https://www.kaggle.com/datasets/mrayushagrawal/us-crime-dataset/data
* Data URL: path = kagglehub.dataset_download("mrayushagrawal/us-crime-dataset")
* Data Type: CSV

The Dataset contains the record of all the crimes in US form 1980.
There are 638454 records and 24 Columns of record. 


## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->
PACKAGES:

Python3

Pandas

NumPy

SQLite3

Kaggle API


## TASK:

1. Extract datasets using Kaggle API: Download unemployment and crime datasets from Kaggle using the kagglehub library. [#1][i1]

2. Data Cleaning and Transformation: Clean and transform the datasets using the pandas library, including converting month names to numeric values and filtering data for the years 2004 to 2014.

3. Loading Data into SQLite: Load the cleaned and merged data into an SQLite database for further analysis.

4. Data Aggregation: Aggregate crime incidents by state and year, summing incidents and calculating mean unemployment rates.

