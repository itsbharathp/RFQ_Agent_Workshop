import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# TODO 1: Import timesfm
# import timesfm

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
    
    # TODO 2: Initialize timesfm.TimesFm
    # Parameters to use:
    # context_len = 32
    # horizon_len = 12
    # input_patch_len = 32
    # output_patch_len = 128
    # num_layers = 20
    # model_dims = 1280
    # backend = "cpu"
    
    # tfm = timesfm.TimesFm(...)
    
    # TODO 3: Load the checkpoint from Hugging Face
    # tfm.load_from_checkpoint(repo_id="google/timesfm-1.0-200m")
    
    # return tfm
    return None

def task_1_commodity_forecast(tfm, prices_df):
    """Forecast Neodymium Magnets prices and detect anomalies."""
    print("\n--- Task 1: Commodity Forecast ---")
    
    # Filter for Neodymium Magnets
    re_df = prices_df[prices_df['commodity'] == 'Neodymium Magnets'].copy()
    re_df = re_df.sort_values('date')
    
    # Split into history (Jan 2024 - Feb 2025) and actuals for testing
    cutoff_date = pd.to_datetime('2025-02-28')
    history_df = re_df[re_df['date'] <= cutoff_date]
    actuals_df = re_df[re_df['date'] > cutoff_date].head(12)
    
    # TODO 4: Run TimesFM forecast_on_df
    # forecast_df = tfm.forecast_on_df(
    #     inputs=history_df,
    #     freq="W",
    #     value_name="price_per_unit",
    #     num_jobs=-1
    # )
    
    # TODO 5: Implement Anomaly Detection
    # Compare actuals_df against the 95% upper bound of the forecast.
    # Generate a list of dictionary alerts for weeks where actual > upper_bound.
    alerts = []
    
    print(f"Generated {len(alerts)} anomaly alerts.")
    return alerts

def task_2_lead_time_forecast(tfm, rfq_df):
    """Forecast average RFQ cycle times."""
    print("\n--- Task 2: Lead Time Forecast ---")
    
    # TODO 6: Calculate cycle time (rfq_deadline - rfq_issue_date in days)
    # TODO 7: Aggregate cycle times by week (mean)
    # TODO 8: Run TimesFM forecast_on_df
    # TODO 9: Plot historical vs forecasted cycle times
    pass

def main():
    prices_df, rfq_df = load_data()
    print("Data loaded successfully.")
    
    # Initialize model
    tfm = init_timesfm()
    if tfm is None:
        print("Please complete TODO 1-3 to initialize TimesFM.")
        return
        
    # Run tasks
    alerts = task_1_commodity_forecast(tfm, prices_df)
    
    with open('shock_alerts.json', 'w') as f:
        json.dump(alerts, f, indent=2)
        
    task_2_lead_time_forecast(tfm, rfq_df)
    
    print("\nChallenge 6 completed!")

if __name__ == "__main__":
    main()