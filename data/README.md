# Vanguard Data Architecture & Provenance

This directory contains the cleaned, validated, and enriched dataset supporting the **Vanguard: Retail Revenue & Customer Decision Intelligence Platform**.

---

## 1. Dataset Provenance & Public Source

- **Dataset Name**: Online Retail Dataset
- **Hosting Institution**: UCI Machine Learning Repository
- **DOI**: [10.24432/C5BW33](https://doi.org/10.24432/C5BW33)
- **Official URL**: [https://archive.ics.uci.edu/dataset/352/online+retail](https://archive.ics.uci.edu/dataset/352/online+retail)
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Original Source**: Transactions from a registered non-store online retail business based in the United Kingdom between 01/12/2010 and 09/12/2011. The company predominantly sells unique all-occasion gift-ware, home accents, and kitchen accessories. Many customers are wholesalers.

---

## 2. Directory Contents

```
data/
├── online_retail.csv        # Primary cleaned & enriched transactional dataset (533,878 records)
├── online_retail.parquet    # High-performance snappy parquet cache for sub-second dashboard loading
└── README.md                # Data documentation and provenance guide
```

---

## 3. Data Schema & Feature Dictionary

| Column Name | Data Type | Description | Analytical Usage |
| :--- | :--- | :--- | :--- |
| `InvoiceNo` | String | 6-digit transaction identifier. Prefixed with `'C'` if cancelled/refunded. | Order volume counting, cancellation tracking |
| `StockCode` | String | 5-digit alphanumeric distinct product SKU code. | Product-level aggregation, SKU Pareto analysis |
| `Description`| String | Cleaned product title / department item. | Product identification, semantic categorization |
| `Quantity` | Integer | Units ordered. Negative values denote customer returns. | Volume metrics, return rate calculations |
| `InvoiceDate`| Datetime | Timestamp of transaction generation (`2010-12-01` to `2011-12-09`). | Time-series forecasting, seasonality heatmaps |
| `UnitPrice` | Float | Product unit price in Sterling (£ / $ normalized). | Unit economics, pricing elasticity analysis |
| `CustomerID` | String | Unique identifier (`CUST-XXXXX`) or `GUEST` for guest checkouts. | RFM customer segmentation, churn analysis |
| `Country` | String | Country of customer domicile (38 distinct markets). | Geographic intelligence, export vs domestic |
| `Category` | String | Department mapped via keyword taxonomy (8 retail categories). | Category performance, product mix analysis |
| `Is_Cancelled`| Boolean | True if transaction is a return or cancellation. | Return-rate risk scoring, refund tracking |
| `Sales` | Float | Net transaction value (`Quantity * UnitPrice`). | Core revenue KPI, monetary scoring |
| `Margin_Rate`| Float | Category-calibrated retail gross margin benchmark (38%–50%). | COGS derivation, profitability modeling |
| `Cost` | Float | Cost of Goods Sold (`Sales * (1 - Margin_Rate)`). | Unit economics, profit margin monitoring |
| `Profit` | Float | Net Gross Profit (`Sales - Cost`). | Profitability KPI, What-If simulation |
| `Year` | Integer | Transaction calendar year (2010 or 2011). | Annual trend analysis |
| `Month` | Integer | Transaction calendar month (1 to 12). | Seasonality modeling |
| `Month_Name` | String | Three-letter month abbreviation (`Jan` to `Dec`). | Chart categorical labeling |
| `YearMonth` | String | Formatted `YYYY-MM` time period. | Monthly trend aggregation, forecasting index |
| `DayOfWeek` | String | Day of week (`Monday` to `Sunday`). | Daily order density heatmaps |
| `Hour` | Integer | Hour of day (0 to 23). | Intraday checkout velocity profiling |
| `Date` | Date | Transaction date component. | Daily cohort and recency calculations |

---

## 4. Preprocessing & Quality Safeguards

1. **Deduplication**: 5,268 exact duplicate records identified and removed.
2. **Missing Value Treatment**: 
   - 1,454 missing product descriptions normalized to `'Unknown Product'`.
   - 135,080 unregistered transactions reconciled under `'GUEST'` profile without discarding valid top-line sales.
3. **Outlier & Code Sanitization**: Non-merchandise administrative codes (`POST`, `D`, `BANK CHARGES`, `AMAZONFEE`, `CRUK`, `PADS`) filtered to preserve retail merchandise integrity.
4. **Economic Logic**: Negative quantity transactions correctly isolated as returns and refunds, rather than falsely counted as regular purchase transactions.
