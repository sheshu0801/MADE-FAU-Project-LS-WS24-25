import os
import sqlite3
import pandas as pd

def run_pipeline():
    os.system('python3 pipeline.py')

def check_output_file():
    return os.path.isfile('/Users/sheshukumar/data/Unemployment_Crime_Data.sqlite')

def check_table_data():
    conn = sqlite3.connect('/Users/sheshukumar/data/Unemployment_Crime_Data.sqlite')
    query = "SELECT * FROM stops"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        return False
    
    # Check data validity
    valid_stop_name = df['stop_name'].apply(lambda x: isinstance(x, str) and bool(re.match(r'^[a-zA-ZäöüÄÖÜß ]+$', x)))
    valid_lat = df['stop_lat'].between(-90, 90)
    valid_lon = df['stop_lon'].between(-90, 90)
    
    return valid_stop_name.all() and valid_lat.all() and valid_lon.all()

def main():
    run_pipeline()
    
    if not check_output_file():
        print("Test failed: Output file does not exist.")
        return
    
    if not check_table_data():
        print("Test failed: Data in the 'stops' table is not valid.")
        return
    
    print("All tests passed.")

if __name__ == "__main__":
    main()
