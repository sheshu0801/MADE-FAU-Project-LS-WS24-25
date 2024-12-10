import os
import pandas as pd
import sqlite3

def run_pipeline():
    os.system('python3 pipeline.py')

def check_output_files():
    csv_path = './data/raw_csv/Yearly_Aggregated_Unemployment_Crime_Data.csv'
    sqlite_path = './data/Unemployment_Crime_Data.sqlite'
    return os.path.isfile(csv_path) and os.path.isfile(sqlite_path)

def check_unemployment_data():
    conn = sqlite3.connect('./data/Unemployment_Crime_Data.sqlite')
    processed_data = pd.read_sql_query("SELECT * FROM YearlyAggregatedUnemploymentCrimeData", conn)
    conn.close()
    
    print(f"Number of records in YearlyAggregatedUnemploymentCrimeData: {len(processed_data)}")
    
    # Check that the DataFrame has the expected number of columns (4)
    assert processed_data.shape[1] == 4, "Table does not have 4 columns"
    
    # Check if columns exist
    expected_columns = ['State', 'Year', 'Percent (%) of Labor Force Unemployed in State/Area', 'Incident']
    for column in expected_columns:
        assert column in processed_data.columns, f"Missing column: {column}"
    
    # Checking data types
    assert pd.api.types.is_string_dtype(processed_data['State']), "State is not a string"
    assert pd.api.types.is_integer_dtype(processed_data['Year']), "Year is not an integer"
    assert pd.api.types.is_float_dtype(processed_data['Percent (%) of Labor Force Unemployed in State/Area']), "Percent (%) of Labor Force Unemployed in State/Area is not a float"
    assert pd.api.types.is_integer_dtype(processed_data['Incident']), "Incident is not an integer"
    
    print("All tests passed for Year[_{{{CITATION{{{_1{](https://github.com/gtfamily/gtfamily/tree/d8389b4fb96ef9ec367a97731351039aa0664e18/plugin.video.SportsDevil%2Flib%2Futils%2FdatetimeUtils.py)
