import os
import pandas as pd
import sqlite3
import kagglehub

class Pipeline:
    def __init__(self):
        
        pass
    def extract_data(self):
        # Downloading datasets using kagglehub
        unemployment_path = kagglehub.dataset_download("justin2028/unemployment-in-america-per-us-state")
        crime_path = kagglehub.dataset_download("mrayushagrawal/us-crime-dataset")
        
        print("Path to unemployment dataset files:", unemployment_path)
        print("Path to crime dataset files:", crime_path)
        
        # Listing files in the directories
        print("Unemployment dataset files:", os.listdir(unemployment_path))
        print("Crime dataset files:", os.listdir(crime_path))
        
        # Moving the datasets to the desired directory
        data_dir = '/Users/sheshukumar/data/raw_csv'
        os.makedirs(data_dir, exist_ok=True)

        # Using the actual file names from the directory listings
        unemployment_data_file = '/Users/sheshukumar/data/raw_csv/Unemployment_in_America.csv'
        crime_data_file = '/Users/sheshukumar/data/raw_csv/US_Crime_DataSet.csv'

        unemployment_data_path = os.path.join(unemployment_path, unemployment_data_file)
        crime_data_path = os.path.join(crime_path, crime_data_file)

        os.rename(unemployment_data_path, os.path.join(data_dir, 'Unemployment_in_America.csv'))
        os.rename(crime_data_path, os.path.join(data_dir, 'US_Crime_DataSet.csv'))

    def transform_data(self):
        # Defining path to CSV files
        unemployment_data_path = '/Users/sheshukumar/data/raw_csv/Unemployment_in_America.csv'
        crime_data_path = '/Users/sheshukumar/data/raw_csv/US_Crime_DataSet.csv'

        df_unemployment = pd.read_csv(unemployment_data_path, delimiter=',')
        df_crime = pd.read_csv(crime_data_path, delimiter=',', low_memory=False)

        # Check and rename columns if necessary
        print("Unemployment Data Columns:", df_unemployment.columns)
        print("Crime Data Columns:", df_crime.columns)

        # Renaming columns to match required names for merging data sets
        if 'State/Area' in df_unemployment.columns:
            df_unemployment.rename(columns={'State/Area': 'State'}, inplace=True)

        if 'Year' not in df_unemployment.columns:
            print("Error: Unemployment data must contain 'Year' column.")
            return

        if 'State' not in df_unemployment.columns:
            print("Error: Unemployment data must contain 'State' column.")
            return

        if 'State' not in df_crime.columns or 'Year' not in df_crime.columns:
            print("Error: Crime data must contain 'State' and 'Year' columns.")
            return

        # Converting columns to appropriate data types
        df_crime['Year'] = pd.to_numeric(df_crime['Year'], errors='coerce')
        df_crime['Victim Age'] = pd.to_numeric(df_crime['Victim Age'], errors='coerce')
        df_crime['Perpetrator Age'] = pd.to_numeric(df_crime['Perpetrator Age'], errors='coerce')

        # Converting month names to numeric values in the crime dataset
        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        df_crime['Month'] = df_crime['Month'].map(month_map)

        # considering data between 2004 and 2014 as the period of interest, and Perpetrator Age above 18 as unemployed
        df_unemployment = df_unemployment[(df_unemployment['Year'] >= 2004) & (df_unemployment['Year'] <= 2014)]
        df_crime = df_crime[(df_crime['Year'] >= 2004) & (df_crime['Year'] <= 2014) & (df_crime['Perpetrator Age'] > 18)]

        # Selecting only the necessary columns
        df_unemployment = df_unemployment[['State', 'Year', 'Month', 'Percent (%) of Labor Force Unemployed in State/Area']]
        df_crime = df_crime[['State', 'Year', 'Month', 'Incident']]

        # Merging dataframes on 'State', 'Year', and 'Month'
        merged_df = pd.merge(df_unemployment, df_crime, how='outer', on=['State', 'Year', 'Month'])
        print("Data transformation complete.")

        # Printing the first few rows of the merged dataframe
        print(merged_df.head())

        # Save the merged dataframe to a CSV file
        merged_df.to_csv('/Users/sheshukumar/data/raw_csv/Merged_Unemployment_Crime_Data.csv', index=False)

        # Save to SQLite
        conn = sqlite3.connect('./data/Unemployment_Crime_Data.sqlite')
        merged_df.to_sql('UnemploymentCrimeData', conn, if_exists='replace', index=False)

        # Verify the data insertion
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM UnemploymentCrimeData")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()
        conn.close()
        print("Data inserted successfully into the database.")

    def query_merged_data(self):
        conn = sqlite3.connect('./data/Unemployment_Crime_Data.sqlite')
        query = "SELECT * FROM UnemploymentCrimeData"
        merged_df = pd.read_sql_query(query, conn)
        print(merged_df.head())
        conn.close()

if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline.extract_data()
    pipeline.transform_data()
    pipeline.query_merged_data()
