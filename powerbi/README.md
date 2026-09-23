# Power BI Report Integration

This directory contains the Power BI metadata and report specifications for **ShopPulse**.

## File Overview

- **`ShopPulse.pbix`**: Power BI desktop report file pre-configured with data models, DAX measures, and theme matching the dashboard design.

## Key DAX Measures Included in Model

```dax
// Total Revenue
Total Revenue = SUM(orders[Sales])

// Total Profit
Total Profit = SUM(orders[Profit])

// Profit Margin %
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0) * 100

// Average Order Value (AOV)
AOV = DIVIDE([Total Revenue], DISTINCTCOUNT(orders[Order_ID]), 0)

// Year-over-Year Revenue Growth
YoY Revenue Growth = 
VAR CurrentYearRevenue = [Total Revenue]
VAR PreviousYearRevenue = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Calendar'[Date]))
RETURN
DIVIDE(CurrentYearRevenue - PreviousYearRevenue, PreviousYearRevenue, 0) * 100
```
