#!/bin/bash

# Running the data pipeline
python3 pipeline.py

# Check if the output CSV file exists
if [ -f "/Users/sheshukumar/data/raw_csv/Yearly_Aggregated_Unemployment_Crime_Data.csv" ]; then
    echo "CSV output file exists. Test passed."
else
    echo "CSV output file does not exist. Test failed."
    exit 1
fi

# Check if the SQLite database exists
if [ -f "./data/Unemployment_Crime_Data.sqlite" ]; then
    echo "SQLite database exists. Test passed."
else
    echo "SQLite database does not exist. Test failed."
    exit 1
fi

echo "All tests passed."
