# System Architecture & Technical Design

## Architecture Overview

**ShopPulse** follows a decoupled 3-tier Business Intelligence architecture:

```
[ Data Storage ] ──> [ Analytics & Preprocessing Engine ] ──> [ Streamlit BI Dashboard ]
   CSV / SQL               backend/analytics.py                   app.py (Plotly)
```

## Layer Breakdown

### 1. Data Layer (`data/`)
- Relational schema stored across 5 CSV files (`orders`, `customers`, `products`, `region`, `payments`).
- Supports relational SQL creation (`database/create_tables.sql`) for PostgreSQL/MySQL scale.

### 2. Analytics Engine (`backend/analytics.py`)
- High-performance Pandas star-schema builder (`load_data`, `preprocess_data`).
- In-memory aggregation caching using Streamlit `@st.cache_resource`.
- Analytical modules:
  - DAX-equivalent metric calculation (`get_kpis()`)
  - Recency-Frequency-Monetary Customer Segmentation (`get_rfm_analysis()`)
  - Profitability What-If Simulator (`get_profitability_analysis()`)
  - Time-series Revenue Forecasting (`get_forecast()`)
  - Natural Language Rule-Based AI Engine (`answer_ai_query()`)

### 3. Presentation Layer (`app.py`)
- Responsive multi-page web layout mimicking Microsoft Power BI & Tableau UI standards.
- Custom injected CSS (`st.markdown`) adhering to Fluent & Dark BI theme tokens.
- Fully interactive Plotly charts with custom color palettes and tooltips.
