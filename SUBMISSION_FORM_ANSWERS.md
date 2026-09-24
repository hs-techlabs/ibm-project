# IBM Project Submission — Quick Copy-Paste Form Guide
**Deadline**: Today  
**Form Link**: [IBM Project Submission Google Form](https://docs.google.com/forms/d/1AnbtsiJVY8QiQEFcgZRfAAQD_C5dz43njkKqpa-YWsg/viewform)  
**GitHub Repository**: [https://github.com/hs-techlabs/ibm-project.git](https://github.com/hs-techlabs/ibm-project.git)

---

## 1. Project Identification

### Project Title
```text
Vanguard — Retail Revenue & Customer Decision Intelligence Platform
```

### Domain / Track
```text
Data Analytics / Business Intelligence / Applied Machine Learning
```

### Problem Statement
```text
Modern international multi-channel retail enterprises face escalating volatility in cross-border logistics, seasonal demand spikes, customer churn, and product return friction. While modern transactional databases log millions of rows, leadership teams frequently operate in analytical silos without real-time driver attribution, customer lifetime segmentation, or dynamic margin sensitivity simulation. Vanguard solves this by turning 533,878 granular international transactions into prioritized, quantitative executive decisions.
```

### Project Summary / Abstract (100–150 words)
```text
Vanguard is an enterprise-grade Decision Intelligence Platform built on a full annual cycle of 533,878 verified transactions across 38 global markets from the UCI Machine Learning Repository. Engineered in Python and Streamlit, the platform operationalizes the end-to-end commercial continuum: Data → Information → Insights → Decisions → Actions. Key capabilities include: 
1. Real-time C-suite KPI attribution net of cancellations and returns ($8.87M net revenue).
2. Algorithmic RFM (Recency, Frequency, Monetary) quintile customer segmentation identifying Champions and At-Risk accounts.
3. Pareto 80/20 product catalog concentration diagnostics.
4. Statistical Holt-Winters time-series revenue forecasting with 95% confidence intervals.
5. Dynamic pricing elasticity and margin sensitivity What-If simulations.
Delivered as a consolidated, reproducible single-file executable (project.py) adhering to IBM project submission guidelines.
```

---

## 2. Technical Stack & Architecture

### Programming Language & Libraries
```text
Python 3.10+, Streamlit, Plotly Express & Graph Objects, Pandas, NumPy, Scikit-Learn, SciPy, PyArrow, OpenPyXL, Python-Docx
```

### Dataset Name & Source
```text
Dataset Name: Online Retail Dataset
Source: UCI Machine Learning Repository
DOI: 10.24432/C5BW33
Direct URL: https://archive.ics.uci.edu/dataset/352/online+retail
License: Creative Commons Attribution 4.0 International (CC BY 4.0)
Scale: 533,878 cleaned records, 38 international markets, 4,372 unique customer cohorts.
```

---

## 3. Key Findings & Business Insights

### Key Project Insights (Copy-paste bullets if requested)
```text
1. Catalog Pareto Rule: The top 20% of catalog SKUs drive 78.4% of total net revenue ($6.95M).
2. Cross-Border Arbitrage: European international orders average $485 AOV—2.1x higher than UK domestic ($228), demonstrating higher fulfillment margin efficiency.
3. Customer Churn Risk: 1,024 high-value accounts ($1.15M baseline replenishment) entered at-risk status, necessitating automated 60-day re-order incentives.
4. Geographic Over-Concentration: 82.4% of topline revenue is domestically UK-dependent, highlighting exposure to local macroeconomic volatility.
```

---

## 4. Deliverable Files & Links for Form Upload

### GitHub Repository Link
```text
https://github.com/hs-techlabs/ibm-project.git
```

### Project Zip File (< 10 MB limit)
- **Recommended File to Upload**: `IBM_Project_Submission.zip` (**8.1 MB**)
  - *Location on your computer*: `/Users/himanshusharma/Downloads/shoppulse-ecommerce-bi-main/IBM_Project_Submission.zip`
  - *Contents*: Complete executable dashboard (`project.py`), full 533k transaction dataset (`online_retail.parquet`), Project Report PDF & DOCX, UI screenshots, requirements.txt, and documentation.
- **Alternative (if portal limit is ≤ 5 MB)**: `IBM_Project_Submission_Lightweight.zip` (**2.7 MB**)
  - *Location on your computer*: `/Users/himanshusharma/Downloads/shoppulse-ecommerce-bi-main/IBM_Project_Submission_Lightweight.zip`

### Project Report File (If requested separately)
- **PDF Report**: `/Users/himanshusharma/Downloads/shoppulse-ecommerce-bi-main/reports/Project_Report.pdf` (1.0 MB)
- **Word Report**: `/Users/himanshusharma/Downloads/shoppulse-ecommerce-bi-main/reports/Project_Report.docx` (1.0 MB)

---

## 5. Setup & Execution Commands (If form asks "How to run")
```bash
git clone https://github.com/hs-techlabs/ibm-project.git
cd ibm-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run project.py
```
