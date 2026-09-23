import os
import pandas as pd
import numpy as np

def clean_data(data_dir=None):
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    
    print("Loading CSV datasets...")
    df_orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    df_customers = pd.read_csv(os.path.join(data_dir, "customers.csv"))
    df_products = pd.read_csv(os.path.join(data_dir, "products.csv"))
    df_region = pd.read_csv(os.path.join(data_dir, "region.csv"))

    # Convert datetimes
    print("Parsing date dimensions...")
    df_orders['Order_Date'] = pd.to_datetime(df_orders['Order_Date'], errors='coerce')
    df_orders['Ship_Date'] = pd.to_datetime(df_orders['Ship_Date'], errors='coerce')
    df_customers['Signup_Date'] = pd.to_datetime(df_customers['Signup_Date'], errors='coerce')

    # Sanitize numeric fields
    print("Sanitizing numerical fields...")
    for col in ['Sales', 'Profit', 'Quantity', 'Cost', 'Discount', 'Unit_Price', 'Shipping_Cost']:
        if col in df_orders.columns:
            df_orders[col] = pd.to_numeric(df_orders[col], errors='coerce').fillna(0)

    # Merge Star Schema
    print("Merging tables into star-schema analytical dataset...")
    merged = df_orders.merge(df_customers, on='Customer_ID', how='left')
    merged = merged.merge(df_products, on='Product_ID', how='left', suffixes=('', '_prod'))

    # Temporal feature engineering
    merged['Year'] = merged['Order_Date'].dt.year
    merged['Month'] = merged['Order_Date'].dt.strftime('%b')
    merged['YearMonth'] = merged['Order_Date'].dt.to_period('M').astype(str)
    merged['DayOfWeek'] = merged['Order_Date'].dt.day_name()
    merged['Hour'] = merged['Order_Date'].dt.hour

    print(f"Cleaned dataset ready: {merged.shape[0]} rows, {merged.shape[1]} columns.")
    return merged

if __name__ == "__main__":
    df_cleaned = clean_data()
    print(df_cleaned.head(3))
