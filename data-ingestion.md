# Data Ingestion Process

## Overview

This document explains how the data ingestion component (`data_ingest.py`) works. The script reads data from a CSV file, applies necessary transformations, and inserts the processed data into the PostgreSQL datastore.

## How It Works

1. **Data Extraction:**
   - The CSV file (`Global_AI_Content_Impact_Dataset.csv`) is read using **pandas**.
   - Data is loaded into a DataFrame for easy manipulation and validation.

2. **Data Transformation:**
   - **Column Renaming:**  
     The CSV columns are mapped to more accessible, snake_case names (e.g., `"AI Adoption Rate (%)"` becomes `ai_adoption_rate`).
   - **Type Conversion:**  
     The `Year` column is converted into a proper datetime type (`published_date`) representing January 1 of that year.
   - **Numeric Conversion and Data Cleaning:**  
     Columns that represent percentages or numerical values (such as `ai_adoption_rate` and `job_loss_due_to_ai`) are converted to native Python numeric types. Rows with missing or invalid entries are dropped to ensure data integrity.
   - **Handling of NumPy Types:**  
     Special care is taken to convert any remaining NumPy data types (e.g., `numpy.datetime64` or `numpy.float64`) into native Python types using methods like `.item()` or `pd.Timestamp(...).to_pydatetime()` to prevent database insertion errors.

3. **Data Insertion:**
   - The script establishes a connection to the PostgreSQL database using **psycopg2**.
   - A bulk insert is performed by transforming the DataFrame into a list of tuples and then using `execute_values` for efficient data insertion.
   - The operation is logged with a confirmation message ("Data ingestion complete!").

## Execution

- **Running the Ingestion Script:**  
  The script can be run as a standalone batch process. In our Dockerized setup, it’s executed by the `ingest` service defined in `docker-compose.yml`.

- **Reusability:**  
  The script is designed to be idempotent; it can be re-run to refresh data or applied periodically via a scheduler.

## Summary

The data ingestion process ensures that raw CSV data is cleaned, transformed, and loaded efficiently into the PostgreSQL database. This prepares the data for subsequent visualization and analysis tasks.

