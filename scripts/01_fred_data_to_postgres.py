"""
Macroeconomic Trend Dashboard Project
Author: Nudrat Hanna Ahona
Date: July 2025

Objective:
Aggregate key macroeconomic indicators (CPI, GDP, Unemployment) into a PostgreSQL database
to enable time series trend analysis, volatility identification, and scenario-based forecasting.

This serves as the foundational data pipeline for index construction and economic regime modeling
aligned with analytical practices at firms like J.P. Morgan.
"""

# Import necessary libraries
from fredapi import Fred
import pandas as pd
from sqlalchemy import create_engine

# Configuration: Replace with your own credentials
FRED_API_KEY = "b9a4903923b9fcb6db345239517e5afc"

DB_USER = "postgres"
DB_PASSWORD = "2002"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "macroindex"

# Initialize FRED connection
fred = Fred(api_key=FRED_API_KEY)

# Define macroeconomic indicators to collect
series_ids = {
    'CPI': 'CPIAUCSL',            # Consumer Price Index
    'GDP': 'GDP',                 # Gross Domestic Product
    'Unemployment': 'UNRATE'      # Unemployment Rate
}

# Collect and format data from FRED
all_data = []

for name, series_id in series_ids.items():
    try:
        series_data = fred.get_series(series_id).reset_index()
        series_data.columns = ['date', 'value']
        series_data['indicator_name'] = name
        all_data.append(series_data)
        print(f"{name} data pulled successfully.")
    except Exception as e:
        print(f"Failed to pull {name}: {e}")

# Concatenate all series into a single DataFrame
df = pd.concat(all_data)

# Display a preview of the combined dataset
print("Preview of combined macroeconomic dataset:")
print(df.head())

# Save data to PostgreSQL
try:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df.to_sql("macro_data", engine, if_exists='replace', index=False)
    print("Data successfully written to PostgreSQL table: macro_data")
except Exception as e:
    print(f"PostgreSQL connection or write failed: {e}")

# Context:
# This script forms the foundation of a macroeconomic research dashboard.
# The data ingested here supports downstream tasks including:
# - Time series forecasting and volatility modeling
# - Scenario-based analysis for index simulation
# - Thematic allocation shifts based on macroeconomic regimes
# - Visualization in Tableau for economic storytelling and insight delivery
