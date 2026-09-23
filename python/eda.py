import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_cleaning import clean_data
import pandas as pd

def run_eda():
    df = clean_data()
    print("\n--- EDA SUMMARY REPORT ---")
    print(f"Total Transactions: {len(df):,}")
    print(f"Date Range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
    print(f"Total Revenue: ${df['Sales'].sum():,.2f}")
    print(f"Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"Overall Profit Margin: {(df['Profit'].sum()/df['Sales'].sum())*100:.2f}%")
    
    print("\n--- Revenue by Category ---")
    cat_summary = df.groupby('Category')[['Sales', 'Profit', 'Quantity']].sum().reset_index()
    cat_summary['Margin %'] = (cat_summary['Profit'] / cat_summary['Sales']) * 100
    print(cat_summary.sort_values(by='Sales', ascending=False).to_string(index=False))

    print("\n--- Top 5 States by Revenue ---")
    state_summary = df.groupby('State')[['Sales', 'Profit']].sum().reset_index()
    print(state_summary.sort_values(by='Sales', ascending=False).head(5).to_string(index=False))

if __name__ == "__main__":
    run_eda()
