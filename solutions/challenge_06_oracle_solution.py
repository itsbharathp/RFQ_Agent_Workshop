import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import timesfm

DATA_DIR = "../../output_v2"

def load_data():
    """Load commodity prices and RFQ events."""
    prices_df = pd.read_csv(os.path.join(DATA_DIR, "03_commodity_prices.csv"))
    rfq_df = pd.read_csv(os.path.join(DATA_DIR, "09_rfq_events.csv"))
    
    # Ensure dates are datetime objects
    prices_df['date'] = pd.to_datetime(prices_df['date'])
    rfq_df['rfq_issue_date'] = pd.to_datetime(rfq_df['rfq_issue_date'])
    rfq_df['rfq_deadline'] = pd.to_datetime(rfq_df['rfq_deadline'])
    
    return prices_df, rfq_df

def init_timesfm():
    """Initialize the TimesFM zero-shot model."""
    print("Initializing TimesFM...")
    
    tfm = timesfm.TimesFm(
        context_len=32,
        horizon_len=12,
        input_patch_len=32,
        output_patch_len=128,
        num_layers=20,
        model_dims=1280,
        backend="cpu"
    )
    
    # Requires HF token setup or local caching
    tfm.load_from_checkpoint(repo_id="google/timesfm-1.0-200m")
    
    return tfm

def task_1_commodity_forecast(tfm, prices_df):
    """Forecast Rare Earth Elements prices and detect anomalies."""
    print("\n--- Task 1: Commodity Forecast ---")
    
    re_df = prices_df[prices_df['commodity_name'] == 'Rare Earth Elements'].copy()
    re_df = re_df.sort_values('date')
    
    # Prepare data for TimesFM (requires 'unique_id' for forecast_on_df)
    re_df['unique_id'] = 'rare_earth'
    
    cutoff_date = pd.to_datetime('2025-02-28')
    history_df = re_df[re_df['date'] <= cutoff_date]
    actuals_df = re_df[re_df['date'] > cutoff_date].head(12)
    
    # Run forecast
    print("Forecasting commodity prices...")
    forecast_df = tfm.forecast_on_df(
        inputs=history_df,
        freq="W",
        value_name="price_per_unit",
        num_jobs=-1
    )
    
    # Extract point forecast and 95% upper bound
    # TimesFM usually outputs columns like: unique_id, ds, TimesFM, TimesFM-q-0.95
    forecast_df = forecast_df.rename(columns={"ds": "date"})
    forecast_df['date'] = pd.to_datetime(forecast_df['date'])
    
    # Merge with actuals
    comparison_df = pd.merge(actuals_df, forecast_df, on="date", how="inner")
    
    alerts = []
    # Using the 90th or 95th quantile depending on TimesFM default quantiles
    upper_bound_col = [c for c in forecast_df.columns if 'q-0.9' in c][-1] 
    
    for _, row in comparison_df.iterrows():
        if row['price_per_unit'] > row[upper_bound_col]:
            alerts.append({
                "date": row['date'].strftime('%Y-%m-%d'),
                "commodity": "Rare Earth Elements",
                "actual_price": float(row['price_per_unit']),
                "forecast_upper_bound": float(row[upper_bound_col]),
                "status": "MARKET_SHOCK_DETECTED"
            })
            
    print(f"Generated {len(alerts)} anomaly alerts.")
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(history_df['date'].tail(30), history_df['price_per_unit'].tail(30), label='Historical')
    plt.plot(comparison_df['date'], comparison_df['price_per_unit'], label='Actual', color='red', marker='x')
    plt.plot(forecast_df['date'], forecast_df['TimesFM'], label='Forecast', color='orange', linestyle='--')
    plt.fill_between(forecast_df['date'], 
                     forecast_df[[c for c in forecast_df.columns if 'q-0.1' in c][0]], 
                     forecast_df[upper_bound_col], 
                     color='orange', alpha=0.2, label='Confidence Interval')
    plt.title('Rare Earth Elements Price Forecast vs Actual')
    plt.legend()
    plt.savefig('commodity_forecast.png')
    plt.close()
    
    return alerts

def task_2_lead_time_forecast(tfm, rfq_df):
    """Forecast average RFQ cycle times."""
    print("\n--- Task 2: Lead Time Forecast ---")
    
    rfq_df['cycle_days'] = (rfq_df['rfq_deadline'] - rfq_df['rfq_issue_date']).dt.days
    rfq_df['week'] = rfq_df['rfq_issue_date'].dt.to_period('W').dt.start_time
    
    weekly_lead = rfq_df.groupby('week')['cycle_days'].mean().reset_index()
    weekly_lead.rename(columns={'week': 'date'}, inplace=True)
    weekly_lead['unique_id'] = 'rfq_cycle'
    
    # Setup for pre-crisis vs crisis
    cutoff_date = pd.to_datetime('2024-09-01')
    history_df = weekly_lead[weekly_lead['date'] <= cutoff_date]
    actuals_df = weekly_lead[weekly_lead['date'] > cutoff_date]
    
    print("Forecasting lead times...")
    forecast_df = tfm.forecast_on_df(
        inputs=history_df,
        freq="W",
        value_name="cycle_days",
        num_jobs=-1
    )
    
    forecast_df = forecast_df.rename(columns={"ds": "date"})
    forecast_df['date'] = pd.to_datetime(forecast_df['date'])
    
    plt.figure(figsize=(10, 5))
    plt.plot(history_df['date'], history_df['cycle_days'], label='Pre-Crisis (Historical)')
    plt.plot(actuals_df['date'].head(12), actuals_df['cycle_days'].head(12), label='Crisis (Actual)', color='red')
    plt.plot(forecast_df['date'], forecast_df['TimesFM'], label='TimesFM Zero-Shot Forecast', color='green', linestyle='--')
    plt.title('RFQ Cycle Time Explosion: Actuals vs Zero-Shot Forecast')
    plt.legend()
    plt.savefig('lead_time_forecast.png')
    plt.close()
    print("Saved lead_time_forecast.png")

def main():
    prices_df, rfq_df = load_data()
    tfm = init_timesfm()
    
    alerts = task_1_commodity_forecast(tfm, prices_df)
    
    with open('shock_alerts.json', 'w') as f:
        json.dump(alerts, f, indent=2)
        
    task_2_lead_time_forecast(tfm, rfq_df)
    print("\nChallenge 6 solutions generated successfully!")

if __name__ == "__main__":
    main()