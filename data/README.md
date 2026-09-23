# Data Directory Guide

This directory contains the dataset used for the ShopPulse E-Commerce Business Intelligence project.

## Directory Structure

```
data/
├── orders.csv             # Sales transactions (Line-level items)
├── customers.csv          # Customer demography and segments
├── products.csv           # Product catalog and pricing
├── region.csv             # Geographic hierarchy (Country, State, City)
├── payments.csv           # Payment methods
└── sample/
    └── sample_data.csv    # Sample data for lightweight testing
```

## Datasets Overview

1. **`orders.csv`** (96,000+ records):
   - `Order_ID`: Unique order identifier
   - `Order_Line_ID`: Unique order line item identifier
   - `Order_Date`: Timestamp of order placement
   - `Ship_Date`: Timestamp of shipping
   - `Customer_ID`: Foreign key to `customers.csv`
   - `Product_ID`: Foreign key to `products.csv`
   - `Quantity`: Units purchased
   - `Unit_Price`: Selling price per unit
   - `Discount`: Discount applied (%)
   - `Sales`: Total sales value after discount
   - `Cost`: Cost of goods sold (COGS)
   - `Profit`: Net profit earned
   - `Shipping_Cost`: Logistics cost
   - `Payment_Method`: Foreign key / payment type string
   - `Order_Status`: Status (`Completed`, `Delivered`, `Shipped`, `Pending`, `Cancelled`)
   - `Sales_Channel`: Channel (`Direct`, `Organic Search`, `Social Media`, `Affiliate`, `Paid Search`)

2. **`customers.csv`**:
   - `Customer_ID`, `Customer_Name`, `Gender`, `Age`, `City`, `State`, `Country`, `Customer_Segment`, `Signup_Date`

3. **`products.csv`**:
   - `Product_ID`, `Product_Name`, `Category`, `Sub_Category`, `Brand`, `Cost`, `List_Price`

4. **`region.csv`**:
   - `Region_ID`, `Country`, `State`, `City`, `Region`

5. **`payments.csv`**:
   - `Payment_ID`, `Payment_Method`
