import os
import pandas as pd
import sqlite3
import requests

class AirQualityAlzheimersPipeline:
    def __init__(self):
        self.data_dir = './data/raw_csv/'
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Paths to save datasets
        self.alz_data_path = os.path.join(self.data_dir, 'Alzheimers_Dataset.csv')
        self.air_quality_data_path = os.path.join(self.data_dir, 'Air_Quality_Dataset.csv')
        
        # Database path
        self.db_path = './data/Alzheimers_AirQuality.sqlite'

    def extract_data(self):
        # URLs for the datasets
        alz_file_url = 'https://data.cdc.gov/api/views/hfr9-rurv/rows.csv?accessType=DOWNLOAD'
        air_quality_file_url = 'https://data.cityofnewyork.us/api/views/c3uy-2p5r/rows.csv?accessType=DOWNLOAD'

        # Download Alzheimer's dataset
        self.download_csv(alz_file_url, self.alz_data_path)

        # Download Air Quality dataset
        self.download_csv(air_quality_file_url, self.air_quality_data_path)

        print("Data extraction complete.")

    def download_csv(self, url, output_path):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded data from {url} to {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")

    def transform_data(self):
        # Loading datasets
        try:
            alz_data = pd.read_csv(self.alz_data_path)
            air_quality_data = pd.read_csv(self.air_quality_data_path)
        except Exception as e:
            print(f"Error loading datasets: {e}")
            return

        # Data Cleaning and Preprocessing
        alz_data.dropna(subset=['LocationAbbr', 'YearStart', 'Data_Value'], inplace=True)
        air_quality_data.dropna(subset=['Geo Join ID', 'Start_Date', 'Data Value'], inplace=True)

        # Transforming Alzheimer's dataset
        alz_data['YearStart'] = alz_data['YearStart'].astype(int)
        alz_data['Data_Value'] = pd.to_numeric(alz_data['Data_Value'], errors='coerce')
        alz_grouped = alz_data.groupby(['LocationAbbr', 'YearStart']).agg({'Data_Value': 'mean'}).reset_index()
        alz_grouped.rename(columns={'Data_Value': 'Alzheimer_Prevalence'}, inplace=True)

        # Transforming Air Quality dataset
        air_quality_data['Start_Date'] = pd.to_datetime(air_quality_data['Start_Date'])
        air_quality_data['Year'] = air_quality_data['Start_Date'].dt.year

        # Example Geo Join ID to Location mapping
        geo_to_state_mapping = {
            '1.0': 'AK', '2.0': 'AL', '3.0': 'AR', '4.0': 'AZ', '5.0': 'CA'  # Update as necessary
        }
        air_quality_data['LocationAbbr'] = air_quality_data['Geo Join ID'].astype(str).map(geo_to_state_mapping)
        air_quality_data.dropna(subset=['LocationAbbr'], inplace=True)
        air_quality_grouped = air_quality_data.groupby(['LocationAbbr', 'Year']).agg({'Data Value': 'mean'}).reset_index()
        air_quality_grouped.rename(columns={'Data Value': 'Pollution_Value'}, inplace=True)

        # Merging datasets
        merged_data = pd.merge(
            alz_grouped,
            air_quality_grouped,
            left_on=['LocationAbbr', 'YearStart'],
            right_on=['LocationAbbr', 'Year'],
            how='inner'
        )
        merged_data.drop(columns=['Year'], inplace=True)

        print("Transformation complete. Sample of merged data:")
        print(merged_data.head())

        # Saving to SQLite database
        conn = sqlite3.connect(self.db_path)
        merged_data.to_sql('AlzheimersAirQuality', conn, if_exists='replace', index=False)
        conn.close()
        print("Data successfully saved to SQLite database.")

    def load_data(self):
        # Load and display data from SQLite database
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM AlzheimersAirQuality"
        data = pd.read_sql(query, conn)
        conn.close()
        print("Data loaded from database:")
        print(data.head())

if __name__ == '__main__':
    pipeline = AirQualityAlzheimersPipeline()
    pipeline.extract_data()
    pipeline.transform_data()
    pipeline.load_data()