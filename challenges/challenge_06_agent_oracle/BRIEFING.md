# Challenge 6 — The Oracle (Zero-Shot Supply Chain Forecasting)

## Context
In late 2024, Meridian Industrial Systems was completely blindsided by a sudden tariff shock, and again in April 2025 by a rare earth materials price spike. Their reactive agents (like the Watchdog and Tactician) handled the fallout efficiently, but Meridian's CFO wants to move from *reactive* to *predictive*. 

They need an "Oracle" to forecast commodity prices and vendor lead times so procurement can pre-buy materials before prices surge or delays compound.

## The Tool: Google TimesFM
Traditional time-series forecasting (ARIMA, LSTMs, Prophet) requires heavy data science lifting, feature engineering, and training—which is too slow for dynamic supply chains. 

Google's **TimesFM** is a Time Series Foundation Model. It performs *zero-shot* forecasting, meaning it can predict Meridian's supply chain trends right out of the box without any model training, using pre-trained weights learned from 100 billion real-world data points.

---

## Objectives

### Task 1: Commodity Price Forecasting & Anomaly Detection
1. **Load Data:** Read `03_commodity_prices.csv`.
2. **Filter:** Extract the weekly prices of "Neodymium Magnets" from Jan 2024 to Feb 2025.
3. **Forecast:** Feed this historical context into TimesFM to forecast the next 12 weeks.
4. **Detect Anomalies:** TimesFM outputs confidence intervals (e.g., 80%, 95%). Write logic to compare the *actual* incoming April 2025 prices against the upper bound of the forecast. When the actual price breaches the 95% confidence interval, trigger a "Market Shock Alert".

### Task 2: Lead Time Expansion Forecasting
1. **Load Data:** Read `09_rfq_events.csv`.
2. **Transform:** Aggregate vendor cycle times (time from issue to deadline/completion) by week.
3. **Forecast:** Use TimesFM to forecast the upcoming 8 weeks of lead times.
4. **Analyze:** Prove whether the model accurately predicts the cascading delays that caused Meridian's Q4 crisis.

---

## Deliverables
1. `oracle.py`: Your completed script based on `starter.py`.
2. `forecast_charts.png`: Visualizations showing historical data, TimesFM forecast horizon, and confidence bounds.
3. `shock_alerts.json`: A generated payload containing the exact weeks where actual values breached the model's bounds.

---

## Getting Started
Ensure you have installed the required dependencies:
```bash
pip install timesfm pandas matplotlib
```

*(Note: TimesFM requires Hugging Face credentials for the first model download. Follow the instructions in `starter.py` if prompted.)*