"""
Macroeconomic Trend Dashboard Project
Author: Nudrat Hanna Ahona
Date: July 2025

Module 2: Forecasting and Volatility Modeling

Objective:
Use Prophet to forecast macroeconomic trends and quantify volatility
to simulate financial churn conditions (e.g., instability in inflation or GDP),
critical for scenario-driven index simulation and investment strategy alignment.
"""

# Import libraries
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import numpy as np

# PostgreSQL connection config
DB_USER = "postgres"
DB_PASSWORD = "202"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "macroindex"

# Step 1: Connect to PostgreSQL and load macroeconomic data
try:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df = pd.read_sql("SELECT * FROM macro_data", engine)
    print("Macro data loaded successfully from PostgreSQL.")
except Exception as e:
    print(f"Error connecting to PostgreSQL or loading data: {e}")
    df = pd.DataFrame()

# Preview the structure of the DataFrame
print("Columns in DataFrame:", df.columns.tolist())
print("Sample data:\n", df.head())

# Step 2: Forecasting parameters
forecast_horizon = 12  # Forecast 12 future monthly points
output = []

# Fix: Use correct column name from your data ('indicator_name' not 'indicator')
indicators = df['indicator_name'].unique()

for indicator in indicators:
    print(f"Processing indicator: {indicator}")

    # Filter data for the current indicator
    temp_df = df[df['indicator_name'] == indicator][['date', 'value']].dropna()
    temp_df = temp_df.sort_values('date')

    # Prophet requires specific column names: 'ds' for date, 'y' for value
    prophet_df = temp_df.rename(columns={'date': 'ds', 'value': 'y'})

    # Step 3: Initialize and train the Prophet model
    model = Prophet(daily_seasonality=False)
    model.fit(prophet_df)

    # Step 4: Create future date range and predict
    future = model.make_future_dataframe(periods=forecast_horizon, freq='M')
    forecast = model.predict(future)

    # Step 5: Calculate rolling volatility (6-month standard deviation)
    prophet_df['rolling_volatility'] = prophet_df['y'].rolling(window=6).std()

    # Step 6: Merge results with volatility
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    result['indicator_name'] = indicator
    result = result.merge(prophet_df[['ds', 'rolling_volatility']], on='ds', how='left')

    output.append(result)

# Step 7: Combine all indicators into one final DataFrame
forecast_df = pd.concat(output)

# Step 8: Export to CSV for Tableau dashboard
forecast_df.to_csv("macro_forecast_volatility.csv", index=False)
print("Forecast and volatility data saved to macro_forecast_volatility.csv")

# Notes:
# - 'ds' = Date
# - 'yhat' = Forecasted value
# - 'rolling_volatility' = Historical trend volatility (used for risk signals)
# This data can be visualized in Tableau to show macro trends, forecast confidence,
# and macro instability periods to simulate index sensitivity or investment risk.
