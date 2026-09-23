import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_cleaning import clean_data
import pandas as pd
import numpy as np

def run_rfm_analysis(save_output=True):
    df = clean_data()
    max_date = df['Order_Date'].max() + pd.Timedelta(days=1)

    rfm = df.groupby('Customer_ID').agg({
        'Order_Date': lambda x: (max_date - x.max()).days,
        'Order_ID': 'nunique',
        'Sales': 'sum'
    }).reset_index()

    rfm.columns = ['Customer_ID', 'Recency', 'Frequency', 'Monetary']

    # Quantile scoring (1 to 5)
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

    # Segment mapping
    def assign_segment(row):
        r, f = int(row['R_Score']), int(row['F_Score'])
        if r >= 4 and f >= 4:
            return 'Champions'
        elif r >= 3 and f >= 3:
            return 'Loyal Customers'
        elif r >= 3 and f < 3:
            return 'Potential Loyalists'
        elif r < 3 and f >= 3:
            return 'At Risk'
        else:
            return 'Lost Customers'

    rfm['Segment'] = rfm.apply(assign_segment, axis=1)

    print("\n--- RFM SEGMENT SUMMARY ---")
    summary = rfm.groupby('Segment').agg(
        Customers=('Customer_ID', 'count'),
        Avg_Recency=('Recency', 'mean'),
        Avg_Frequency=('Frequency', 'mean'),
        Avg_Monetary=('Monetary', 'mean')
    ).reset_index()
    print(summary.to_string(index=False))

    if save_output:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "customer_rfm.csv")
        rfm.to_csv(out_path, index=False)
        print(f"\nSaved RFM results to: {out_path}")

    return rfm

if __name__ == "__main__":
    run_rfm_analysis()
