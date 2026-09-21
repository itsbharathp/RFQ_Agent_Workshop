# Challenge 6 — The Oracle (TimesFM) Solution Guide

## Overview
This challenge introduces Google's **TimesFM**, a zero-shot foundation model for time series forecasting. Unlike traditional models that require extensive training and feature engineering (like LSTMs or ARIMA), TimesFM can take raw time series data and immediately project future values with confidence intervals based on its pre-training across billions of data points.

## Task 1: Commodity Price Anomaly Detection
In Task 1, the goal is to forecast the price of "Rare Earth Elements" right before the major price spike in April 2025. 

### Why this matters
Meridian's previous agents (The Watchdog and The Tactician) reacted *after* the prices spiked. An Oracle agent anticipates the spike. 

### The Solution Logic
1. **Prepare the DataFrame:** TimesFM's `forecast_on_df` requires a specific format containing a `unique_id` column, a date column, and the target value column.
2. **Forecast Generation:** We feed the historical data (up to Feb 2025) into the model with a horizon of 12 weeks.
3. **Anomaly Extraction:** TimesFM automatically generates quantiles (e.g., `TimesFM-q-0.9`). The solution script merges the actual incoming April data with the forecast. When the actual price exceeds the upper confidence bound (`q-0.9` or `q-0.95`), the script generates a `MARKET_SHOCK_DETECTED` JSON alert.

These JSON alerts can then be piped into an Agent's context window, allowing a Claude-powered Tactician to preemptively secure inventory.

## Task 2: Lead Time Expansion
In Task 2, we forecast RFQ cycle times just as the September 2024 tariff shock hits. 

### The Insight
If you run the solution script and view `lead_time_forecast.png`, you'll notice something interesting: **The zero-shot forecast likely does *not* predict the massive explosion in lead times.** 

Why? Because TimesFM relies on historical patterns. Since Meridian's cycle times were stable for 9 months, a purely statistical univariate model assumes they will remain stable. 

**This is the crux of the lesson:** Univariate time-series forecasting is exceptional for stable commodities and seasonal trends, but it is blind to exogenous causal events (like a sudden geopolitical tariff). This proves to participants that statistical forecasting (The Oracle) must be combined with causal reasoning and market signal parsing (The Tactician) to build a truly resilient supply chain. 

## Expected Outputs
Running the solution script should produce:
1. `commodity_forecast.png` - Showing the price breaking the upper bounds.
2. `lead_time_forecast.png` - Showing the actual lead times diverging massively from the statistical forecast.
3. `shock_alerts.json` - A list of anomalies formatted for agent consumption.