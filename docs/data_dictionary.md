# Data Dictionary

## Table 1: `orders.csv`
| Column Name | Data Type | Nullable | Description |
|---|---|---|---|
| `Order_ID` | String (VARCHAR) | No | Unique identifier for the order transaction |
| `Order_Line_ID` | String (VARCHAR) | No | Primary key for order item line |
| `Order_Date` | Timestamp | No | Date and time when order was placed |
| `Ship_Date` | Timestamp | Yes | Date and time when order was shipped |
| `Customer_ID` | String (VARCHAR) | No | Foreign Key to `customers.csv` |
| `Product_ID` | String (VARCHAR) | No | Foreign Key to `products.csv` |
| `Quantity` | Integer | No | Number of units purchased |
| `Unit_Price` | Decimal | No | Listed unit price |
| `Discount` | Decimal | No | Discount fraction applied (0.0 to 1.0) |
| `Sales` | Decimal | No | Net revenue generated after discount |
| `Cost` | Decimal | No | Cost of Goods Sold (COGS) |
| `Profit` | Decimal | No | Net profit earned (`Sales - Cost`) |
| `Shipping_Cost` | Decimal | Yes | Freight/shipping fee |
| `Payment_Method` | String | Yes | Payment method used |
| `Order_Status` | String | No | Fulfillment status (`Completed`, `Delivered`, `Shipped`, `Pending`, `Cancelled`) |
| `Sales_Channel` | String | No | Acquisition channel |

## Table 2: `customers.csv`
| Column Name | Data Type | Nullable | Description |
|---|---|---|---|
| `Customer_ID` | String (VARCHAR) | No | Primary key for customer |
| `Customer_Name` | String | No | Full name |
| `Gender` | String | Yes | Gender |
| `Age` | Integer | Yes | Customer age |
| `City` | String | Yes | Customer city |
| `State` | String | Yes | Customer state |
| `Country` | String | Yes | Customer country |
| `Customer_Segment` | String | No | Segment (`Consumer`, `Corporate`, `Home Office`, `Small Business`) |
| `Signup_Date` | Date | Yes | Account creation date |

## Table 3: `products.csv`
| Column Name | Data Type | Nullable | Description |
|---|---|---|---|
| `Product_ID` | String (VARCHAR) | No | Primary key for product |
| `Product_Name` | String | No | Product title |
| `Category` | String | No | Top-level product category |
| `Sub_Category` | String | Yes | Sub-category classification |
| `Brand` | String | Yes | Manufacturer brand |
| `Cost` | Decimal | No | Standard unit cost |
| `List_Price` | Decimal | No | Standard unit list price |
