"""
Macroeconomic Trend Dashboard Project
Author: Nudrat Hanna Ahona
Date: July 2025

Module 3: Simulate Index Logic

Objective:
Generate portfolio allocation weights across asset classes (Equities, Bonds, Commodities, Cash)
based on forecasted macroeconomic conditions using simple rule-based logic.

This simulates how an investment index or strategy may realign under different economic regimes—
similar to thematic or tactical asset allocation models used in index construction.
"""

import pandas as pd

# Load the macroeconomic forecast data (from Module 2)
try:
    forecast_df = pd.read_csv("macro_forecast_volatility.csv")
    print("Forecast data loaded successfully.")
except Exception as e:
    print(f"Error loading forecast data: {e}")
    exit()

# Ensure no missing values in key columns
forecast_df = forecast_df.dropna(subset=['yhat'])

# Pivot to have each indicator (CPI, GDP, Unemployment) as a column
pivot_df = forecast_df.pivot(index="ds", columns="indicator_name", values="yhat").reset_index()
pivot_df.columns.name = None  # remove pivot table index name

# Forward fill missing values (if any)
pivot_df = pivot_df.fillna(method="ffill")

# Define rule-based logic for asset allocation
def assign_weights(row):
    cpi = row.get("CPI", 0)
    gdp = row.get("GDP", 0)
    unemp = row.get("Unemployment", 0)

    # Default (neutral) weights
    equities, bonds, commodities, cash = 0.5, 0.3, 0.1, 0.1

    # Rule 1: High inflation + low growth → overweight commodities
    if cpi > 6 and gdp < 2:
        equities, bonds, commodities, cash = 0.2, 0.2, 0.5, 0.1

    # Rule 2: High GDP growth → overweight equities
    elif gdp > 3:
        equities, bonds, commodities, cash = 0.6, 0.3, 0.05, 0.05

    # Rule 3: High unemployment → increase bonds and cash
    elif unemp > 7:
        equities, bonds, commodities, cash = 0.2, 0.5, 0.1, 0.2

    return pd.Series({
        "Equities": equities,
        "Bonds": bonds,
        "Commodities": commodities,
        "Cash": cash
    })

# Apply the rule-based logic
weights_df = pivot_df.apply(assign_weights, axis=1)

# Combine weights with corresponding dates
simulated_index_df = pd.concat([pivot_df[['ds']], weights_df], axis=1)

# Save the result to CSV for visualization
simulated_index_df.to_csv("index_simulation.csv", index=False)
print("Simulated index allocation saved to index_simulation.csv")

# Context:
# This dataset represents how a portfolio would realign based on economic regime signals.
# It can be used in Tableau to visualize allocation shifts over time in response to macro trends.

