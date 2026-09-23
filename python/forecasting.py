import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_cleaning import clean_data
import pandas as pd
import numpy as np

def run_forecasting(months_ahead=6, save_output=True):
    df = clean_data()
    monthly = df.groupby('YearMonth')['Sales'].sum().reset_index()
    monthly.columns = ['YearMonth', 'Revenue']
    monthly['Month_Index'] = np.arange(len(monthly))

    # Linear trend fit
    poly = np.polyfit(monthly['Month_Index'], monthly['Revenue'], 1)
    slope, intercept = poly[0], poly[1]

    future_indices = np.arange(len(monthly), len(monthly) + months_ahead)
    last_period = pd.Period(monthly['YearMonth'].iloc[-1], freq='M')
    future_periods = [(last_period + i).strftime('%Y-%m') for i in range(1, months_ahead + 1)]

    future_revenue = slope * future_indices + intercept

    # Recent historical average growth adjustment
    recent_growth = (monthly['Revenue'].iloc[-1] - monthly['Revenue'].iloc[0]) / len(monthly)
    future_revenue = np.maximum(future_revenue + recent_growth * 0.2, 0)

    df_hist = monthly[['YearMonth', 'Revenue']].copy()
    df_hist['Type'] = 'Historical'

    df_future = pd.DataFrame({
        'YearMonth': future_periods,
        'Revenue': future_revenue,
        'Type': 'Forecast'
    })

    forecast_df = pd.concat([df_hist, df_future], ignore_index=True)

    print(f"\n--- {months_ahead}-MONTH REVENUE FORECAST ---")
    print(df_future.to_string(index=False))

    if save_output:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "forecast_output.csv")
        forecast_df.to_csv(out_path, index=False)
        print(f"\nSaved forecast results to: {out_path}")

    return forecast_df

if __name__ == "__main__":
    run_forecasting()
