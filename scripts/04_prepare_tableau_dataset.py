"""
Macroeconomic Trend Dashboard Project
Author: Nudrat Hanna Ahona
Date: July 2025

Module 4: Prepare Dataset for Tableau

Objective:
Merge macro forecasts, volatility metrics, and simulated index weights
into one flat file for visual analysis and dashboarding in Tableau.
"""

import pandas as pd

# Load forecast data with volatility
try:
    forecast = pd.read_csv("macro_forecast_volatility.csv")
    print("Forecast and volatility data loaded.")
except Exception as e:
    print(f"Error loading macro forecast file: {e}")
    exit()

# Load index simulation output
try:
    weights = pd.read_csv("index_simulation.csv")
    print("Simulated index weights loaded.")
except Exception as e:
    print(f"Error loading index weights file: {e}")
    exit()

# Pivot forecast to get indicators in columns (CPI, GDP, Unemployment)
macro = forecast.pivot(index="ds", columns="indicator_name", values="yhat").reset_index()
macro.columns.name = None

# Pivot rolling volatility to get volatility columns
vol = forecast.pivot(index="ds", columns="indicator_name", values="rolling_volatility").reset_index()
vol.columns.name = None
vol = vol.rename(columns={
    "CPI": "CPI_volatility",
    "GDP": "GDP_volatility",
    "Unemployment": "Unemployment_volatility"
})

# Merge all together on date
merged = pd.merge(macro, vol, on="ds", how="left")
merged = pd.merge(merged, weights, on="ds", how="left")

# Optional: Convert date to datetime and sort
merged['ds'] = pd.to_datetime(merged['ds'])
merged = merged.sort_values("ds")

# Save the final Tableau-ready dataset
merged.to_csv("tableau_dashboard_data.csv", index=False)
print("✅ Saved clean Tableau dataset: tableau_dashboard_data.csv")

# This dataset can be used to:
# - Plot macro trends and volatility over time
# - Visualize index weight shifts
# - Filter by economic regime, forecast date range, and more
