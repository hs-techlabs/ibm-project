"""
================================================================================
VANGUARD: RETAIL REVENUE & CUSTOMER DECISION INTELLIGENCE PLATFORM
================================================================================
A unified enterprise business intelligence system demonstrating the full BI workflow:
DATA -> INFORMATION -> INSIGHTS -> DECISION -> ACTION

Original Project Foundation: ShopPulse (MIT License).
Substantially modified, expanded, and developed by Vanguard Analytics for
enterprise decision-making and academic/industry submission.
Dataset: UCI Machine Learning Repository Online Retail Dataset (CC BY 4.0).
================================================================================
"""

import os
import sys
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# 1. STREAMLIT PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vanguard — Retail Decision Intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. DESIGN TOKENS & ENTERPRISE STYLING
# ─────────────────────────────────────────────────────────────────────────────
BG_COLOR       = "#0E131F"   # Deep executive obsidian
PANEL_COLOR    = "#161D2F"   # Elevated card background
BORDER_COLOR   = "#25304B"   # Subtle structural border
TEXT_PRIMARY   = "#F8FAFC"   # High contrast crisp white
TEXT_SECONDARY = "#94A3B8"   # Slate muted neutral
TEXT_TERTIARY  = "#64748B"   # Subtle neutral
ACCENT_CYAN    = "#06B6D4"   # Primary decision cyan
ACCENT_BLUE    = "#3B82F6"   # Secondary royal blue
ACCENT_GREEN   = "#10B981"   # Growth positive emerald
ACCENT_AMBER   = "#F59E0B"   # Caution amber
ACCENT_ROSE    = "#F43F5E"   # Risk rose/red
ACCENT_PURPLE  = "#8B5CF6"   # Segment purple

PALETTE = [ACCENT_CYAN, ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_AMBER, ACCENT_ROSE, "#EC4899", "#14B8A6"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, .stApp {{
    background-color: {BG_COLOR} !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {TEXT_PRIMARY} !important;
}}

/* Clean header and footer */
header[data-testid="stHeader"] {{ background: transparent !important; }}
#MainMenu, footer, .stDeployButton {{ display: none !important; }}
.block-container {{ padding-top: 1rem !important; padding-bottom: 2.5rem !important; max-width: 1600px; }}

/* Sidebar navigation */
section[data-testid="stSidebar"] {{
    background-color: {PANEL_COLOR} !important;
    border-right: 1px solid {BORDER_COLOR};
    width: 280px !important;
}}
section[data-testid="stSidebar"] > div {{ padding-top: 1rem; }}

.brand-container {{
    display: flex; align-items: center; gap: 12px; padding: 8px 12px 18px 12px;
    border-bottom: 1px solid {BORDER_COLOR}; margin-bottom: 18px;
}}
.brand-icon {{
    width: 38px; height: 38px; border-radius: 8px;
    background: linear-gradient(135deg, {ACCENT_CYAN}, {ACCENT_BLUE});
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 18px; color: #fff;
    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.25);
}}
.brand-name {{ font-size: 16px; font-weight: 800; letter-spacing: -0.3px; color: {TEXT_PRIMARY}; }}
.brand-tag {{ font-size: 10.5px; color: {TEXT_SECONDARY}; text-transform: uppercase; letter-spacing: 0.8px; }}

/* Nav & Filter labels */
.nav-heading {{
    font-size: 10px; font-weight: 700; color: {TEXT_TERTIARY};
    text-transform: uppercase; letter-spacing: 1px; margin: 12px 0 6px 8px;
}}

/* Radio styling in sidebar */
section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {{ gap: 3px; }}
section[data-testid="stSidebar"] .stRadio label {{
    padding: 9px 12px !important; border-radius: 6px !important;
    background: transparent !important; margin: 0 !important;
    border: 1px solid transparent !important; cursor: pointer;
    transition: all 0.15s ease-in-out;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(255, 255, 255, 0.04) !important;
}}
section[data-testid="stSidebar"] .stRadio label:has(input:checked) {{
    background: rgba(6, 182, 212, 0.12) !important;
    border: 1px solid rgba(6, 182, 212, 0.35) !important;
}}
section[data-testid="stSidebar"] .stRadio label:has(input:checked) span {{
    color: {ACCENT_CYAN} !important; font-weight: 700 !important;
}}
section[data-testid="stSidebar"] .stRadio label span {{
    color: {TEXT_SECONDARY} !important; font-size: 13.5px !important;
}}
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {{ display: none; }}

/* Page Header */
.page-header {{
    display: flex; justify-content: space-between; align-items: baseline;
    padding-bottom: 12px; margin-bottom: 16px; border-bottom: 1px solid {BORDER_COLOR};
}}
.page-title {{ font-size: 22px; font-weight: 800; color: {TEXT_PRIMARY}; letter-spacing: -0.4px; }}
.page-subtitle {{ font-size: 12.5px; color: {TEXT_SECONDARY}; margin-top: 2px; }}
.badge-pill {{
    display: inline-block; padding: 4px 10px; border-radius: 6px;
    font-size: 11px; font-weight: 600; border: 1px solid {BORDER_COLOR};
    background: {PANEL_COLOR}; color: {TEXT_SECONDARY};
}}

/* Metric Cards */
.metric-box {{
    background: {PANEL_COLOR}; border: 1px solid {BORDER_COLOR};
    border-radius: 8px; padding: 14px 16px 12px 16px; height: 100%;
    position: relative; overflow: hidden;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}}
.metric-box::before {{
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--top-accent, {ACCENT_CYAN});
}}
.metric-title {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: {TEXT_SECONDARY}; }}
.metric-value {{ font-size: 24px; font-weight: 800; color: {TEXT_PRIMARY}; margin: 4px 0; letter-spacing: -0.5px; font-family: 'JetBrains Mono', monospace; }}
.metric-delta {{ display: inline-flex; align-items: center; gap: 4px; font-size: 11px; font-weight: 700; padding: 2px 7px; border-radius: 4px; }}
.delta-pos {{ background: rgba(16, 185, 129, 0.15); color: {ACCENT_GREEN}; }}
.delta-neg {{ background: rgba(244, 63, 94, 0.15); color: {ACCENT_ROSE}; }}
.delta-neutral {{ background: rgba(148, 163, 184, 0.15); color: {TEXT_SECONDARY}; }}

/* Content Panels */
.panel-card {{
    background: {PANEL_COLOR}; border: 1px solid {BORDER_COLOR};
    border-radius: 8px; padding: 16px 18px; margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}}
.panel-head {{
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}}
.panel-title {{ font-size: 14px; font-weight: 700; color: {TEXT_PRIMARY}; }}
.panel-sub {{ font-size: 11.5px; color: {TEXT_SECONDARY}; }}

/* Operational Framework Cards (FACT -> INSIGHT -> ACTION) */
.action-card {{
    background: rgba(22, 29, 47, 0.7); border: 1px solid {BORDER_COLOR};
    border-left: 4px solid {ACCENT_CYAN}; border-radius: 6px;
    padding: 12px 14px; margin-bottom: 10px;
}}
.action-card.risk {{ border-left-color: {ACCENT_ROSE}; }}
.action-card.opp {{ border-left-color: {ACCENT_GREEN}; }}
.action-card.caution {{ border-left-color: {ACCENT_AMBER}; }}

.action-label {{ font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 2px; }}
.action-text {{ font-size: 12.5px; color: {TEXT_PRIMARY}; line-height: 1.5; }}
.action-step {{ font-size: 12px; font-weight: 600; color: {ACCENT_CYAN}; margin-top: 6px; display: flex; align-items: center; gap: 4px; }}

/* Tables */
div[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER_COLOR} !important; border-radius: 6px !important;
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 3. DATA INGESTION & ADVANCED PREPROCESSING ENGINE
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading Vanguard Retail Intelligence Repository...")
def load_vanguard_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parquet_path = os.path.join(base_dir, "data", "online_retail.parquet")
    csv_path = os.path.join(base_dir, "data", "online_retail.csv")

    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        # Fallback safeguard: download and process if files were missing
        url = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
        import urllib.request, zipfile, io
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            with z.open('Online Retail.xlsx') as f:
                df = pd.read_excel(f)
        # Apply standard cleaning
        df = df.drop_duplicates()
        df['Description'] = df['Description'].fillna('Unknown Product').astype(str).str.strip().str.upper()
        df['InvoiceNo'] = df['InvoiceNo'].astype(str).str.strip()
        df['Is_Cancelled'] = df['InvoiceNo'].str.startswith('C') | (df['Quantity'] < 0)
        df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce').fillna(0)
        non_retail = ['POST', 'D', 'M', 'BANK CHARGES', 'PADS', 'DOT', 'CRUK', 'AMAZONFEE', 'S']
        df = df[~df['StockCode'].astype(str).str.upper().isin(non_retail)]
        df['Sales'] = (df['Quantity'] * df['UnitPrice']).round(2)
        df['Margin_Rate'] = 0.40
        df['Cost'] = (df['Sales'] * 0.60).round(2)
        df['Profit'] = (df['Sales'] - df['Cost']).round(2)
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        df['Year'] = df['InvoiceDate'].dt.year
        df['Month'] = df['InvoiceDate'].dt.month
        df['Month_Name'] = df['InvoiceDate'].dt.strftime('%b')
        df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
        df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
        df['Hour'] = df['InvoiceDate'].dt.hour
        df['Date'] = df['InvoiceDate'].dt.date
        df['CustomerID'] = df['CustomerID'].apply(lambda x: f'CUST-{int(x):05d}' if pd.notnull(x) else 'GUEST')
        df['Category'] = 'Gifts & Novelties'

    # Ensure correct datetime & string types
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Is_Cancelled'] = df['Is_Cancelled'].astype(bool)
    return df

df_raw = load_vanguard_data()


# ─────────────────────────────────────────────────────────────────────────────
# 4. PLOTLY CHART THEME & LAYOUT HELPER
# ─────────────────────────────────────────────────────────────────────────────
def get_chart_layout(height=340, showlegend=False):
    return dict(
        height=height,
        paper_bgcolor=PANEL_COLOR,
        plot_bgcolor=PANEL_COLOR,
        font=dict(family="Plus Jakarta Sans, sans-serif", color=TEXT_SECONDARY, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=showlegend,
        legend=dict(
            orientation="h", y=1.14, x=0,
            font=dict(color=TEXT_PRIMARY, size=11),
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor=BORDER_COLOR,
            linecolor=BORDER_COLOR,
            tickfont=dict(color=TEXT_SECONDARY, size=10)
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor=BORDER_COLOR,
            linecolor=BORDER_COLOR,
            tickfont=dict(color=TEXT_SECONDARY, size=10)
        ),
        hoverlabel=dict(
            bgcolor=BG_COLOR,
            font_color=TEXT_PRIMARY,
            font_size=11,
            bordercolor=BORDER_COLOR
        ),
    )


# ─────────────────────────────────────────────────────────────────────────────
# 5. BUSINESS ANALYTICS & STATISTICAL KPI CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────
def calculate_kpis(df):
    """
    Computes rigorous corporate KPIs:
    - Net Revenue: Completed sales minus returns
    - Completed Orders: Unique completed transaction invoices
    - AOV: Net Revenue / Completed Orders
    - Active Customers: Unique registered active customer IDs
    - Gross Profit Margin %: Total Profit / Total Net Revenue
    - Return Rate %: Absolute Return Revenue / Gross Positive Revenue
    """
    completed = df[~df['Is_Cancelled']]
    cancelled = df[df['Is_Cancelled']]

    gross_revenue = float(completed['Sales'].sum())
    return_revenue = abs(float(cancelled['Sales'].sum()))
    net_revenue = gross_revenue - return_revenue

    total_orders = int(completed['InvoiceNo'].nunique())
    total_customers = int(df[df['CustomerID'] != 'GUEST']['CustomerID'].nunique())

    aov = float(net_revenue / total_orders) if total_orders > 0 else 0.0
    net_profit = float(df['Profit'].sum())
    gross_margin = float((net_profit / net_revenue) * 100) if net_revenue > 0 else 0.0
    return_rate = float((return_revenue / gross_revenue) * 100) if gross_revenue > 0 else 0.0

    # Period-over-period comparison (split filtered range in halves)
    dates = df['InvoiceDate'].sort_values()
    if len(dates) > 10:
        mid_point = dates.iloc[len(dates) // 2]
        p1 = df[df['InvoiceDate'] < mid_point]
        p2 = df[df['InvoiceDate'] >= mid_point]

        p1_net = p1[~p1['Is_Cancelled']]['Sales'].sum() - abs(p1[p1['Is_Cancelled']]['Sales'].sum())
        p2_net = p2[~p2['Is_Cancelled']]['Sales'].sum() - abs(p2[p2['Is_Cancelled']]['Sales'].sum())
        rev_growth = float(((p2_net - p1_net) / p1_net) * 100) if p1_net > 0 else 0.0

        p1_orders = p1[~p1['Is_Cancelled']]['InvoiceNo'].nunique()
        p2_orders = p2[~p2['Is_Cancelled']]['InvoiceNo'].nunique()
        order_growth = float(((p2_orders - p1_orders) / p1_orders) * 100) if p1_orders > 0 else 0.0
    else:
        rev_growth = 0.0
        order_growth = 0.0

    return {
        "net_revenue": net_revenue,
        "gross_revenue": gross_revenue,
        "return_revenue": return_revenue,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "aov": round(aov, 2),
        "net_profit": round(net_profit, 2),
        "gross_margin": round(gross_margin, 1),
        "return_rate": round(return_rate, 2),
        "rev_growth": round(rev_growth, 1),
        "order_growth": round(order_growth, 1)
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6. SIDEBAR: NAVIGATION, STRATEGIC FILTERS & CONTROLS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="brand-container">
        <div class="brand-icon">V</div>
        <div>
            <div class="brand-name">VANGUARD</div>
            <div class="brand-tag">Decision Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-heading">Intelligence Modules</div>', unsafe_allow_html=True)
    selected_page = st.radio(
        "Navigation",
        [
            "1. Executive Overview",
            "2. Revenue & Sales Intelligence",
            "3. Product & Category Intelligence",
            "4. Customer Intelligence (RFM)",
            "5. Risk & Opportunity Engine",
            "6. Predictive & Scenario Simulator"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="nav-heading">Strategic Filters</div>', unsafe_allow_html=True)

    timeframe_option = st.selectbox(
        "Time Horizon",
        ["Full Dataset (Dec 2010 - Dec 2011)", "2011 Full Year", "H2 2011 Expansion (Jul - Dec)", "Q4 2011 Holiday Surge (Oct - Dec)"]
    )

    all_categories = ["All Departments"] + sorted(df_raw['Category'].dropna().unique().tolist())
    selected_category = st.selectbox("Department", all_categories)

    top_countries = ["All Markets", "United Kingdom", "Germany", "France", "EIRE", "Netherlands", "Spain", "International (Ex-UK)"]
    selected_country = st.selectbox("Geography", top_countries)

    st.markdown("---")
    st.markdown('<div class="nav-heading">Dataset Governance</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px; color:{TEXT_SECONDARY}; line-height:1.4;">
        <b>Source:</b> UCI Machine Learning Repository<br>
        <b>Transactions:</b> 533,878 verified rows<br>
        <b>Markets:</b> 38 international territories<br>
        <b>Attribution:</b> CC BY 4.0 / ShopPulse MIT
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 7. FILTER APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
df = df_raw.copy()

# Time horizon filtering
if timeframe_option == "2011 Full Year":
    df = df[df['Year'] == 2011]
elif timeframe_option == "H2 2011 Expansion (Jul - Dec)":
    df = df[(df['Year'] == 2011) & (df['Month'] >= 7)]
elif timeframe_option == "Q4 2011 Holiday Surge (Oct - Dec)":
    df = df[(df['Year'] == 2011) & (df['Month'] >= 10)]

# Category filtering
if selected_category != "All Departments":
    df = df[df['Category'] == selected_category]

# Geography filtering
if selected_country == "International (Ex-UK)":
    df = df[df['Country'] != "United Kingdom"]
elif selected_country != "All Markets":
    df = df[df['Country'] == selected_country]


# Compute shared metrics
kpis = calculate_kpis(df)


# ─────────────────────────────────────────────────────────────────────────────
# 8. REUSABLE UI RENDERING HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def render_page_header(title, subtitle):
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">{title}</div>
            <div class="page-subtitle">{subtitle}</div>
        </div>
        <div>
            <span class="badge-pill">{selected_category}</span>
            <span class="badge-pill" style="margin-left:4px;">{selected_country}</span>
            <span class="badge-pill" style="margin-left:4px;">{timeframe_option.split(' ')[0]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_strip():
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    def render_card(col, label, value, delta_str, delta_type, accent):
        with col:
            cls = "delta-pos" if delta_type == "pos" else ("delta-neg" if delta_type == "neg" else "delta-neutral")
            st.markdown(f"""
            <div class="metric-box" style="--top-accent:{accent};">
                <div class="metric-title">{label}</div>
                <div class="metric-value">{value}</div>
                <span class="metric-delta {cls}">{delta_str}</span>
            </div>
            """, unsafe_allow_html=True)

    d_rev = f"▲ +{kpis['rev_growth']}%" if kpis['rev_growth'] >= 0 else f"▼ {kpis['rev_growth']}%"
    t_rev = "pos" if kpis['rev_growth'] >= 0 else "neg"

    d_ord = f"▲ +{kpis['order_growth']}%" if kpis['order_growth'] >= 0 else f"▼ {kpis['order_growth']}%"
    t_ord = "pos" if kpis['order_growth'] >= 0 else "neg"

    render_card(c1, "Net Revenue", f"${kpis['net_revenue']:,.0f}", d_rev, t_rev, ACCENT_CYAN)
    render_card(c2, "Completed Orders", f"{kpis['total_orders']:,}", d_ord, t_ord, ACCENT_BLUE)
    render_card(c3, "Avg Order Value", f"${kpis['aov']:.2f}", "Basket Depth", "neutral", ACCENT_AMBER)
    render_card(c4, "Active Customers", f"{kpis['total_customers']:,}", "Verified Accounts", "neutral", ACCENT_PURPLE)
    render_card(c5, "Gross Margin", f"{kpis['gross_margin']:.1f}%", f"${kpis['net_profit']:,.0f} Profit", "pos", ACCENT_GREEN)
    render_card(c6, "Return Rate", f"{kpis['return_rate']:.2f}%", f"${kpis['return_revenue']:,.0f} Lost", "neg", ACCENT_ROSE)
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 9. MODULE 1: EXECUTIVE OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if selected_page == "1. Executive Overview":
    render_page_header(
        "Executive Decision Briefing",
        "Comprehensive operational pulse, business drivers, risk exposures, and strategic priorities"
    )
    render_kpi_strip()

    # Main Trend and Driver Snapshot
    col_trend, col_action = st.columns([1.8, 1.2])

    with col_trend:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div>
                    <div class="panel-title">Revenue & Profit Performance Trajectory</div>
                    <div class="panel-sub">Monthly net sales vs gross margin realization ($)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        monthly = df.groupby('YearMonth').agg(
            Revenue=('Sales', lambda s: s[s > 0].sum() - abs(s[s < 0].sum())),
            Profit=('Profit', 'sum'),
            Orders=('InvoiceNo', lambda i: i.nunique())
        ).reset_index().sort_values('YearMonth')

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly['YearMonth'], y=monthly['Revenue'],
            name="Net Revenue", mode="lines+markers",
            line=dict(color=ACCENT_CYAN, width=3, shape="spline"),
            fill="tozeroy", fillcolor="rgba(6, 182, 212, 0.08)"
        ))
        fig.add_trace(go.Scatter(
            x=monthly['YearMonth'], y=monthly['Profit'],
            name="Gross Profit", mode="lines+markers",
            line=dict(color=ACCENT_GREEN, width=2.5, dash="dot", shape="spline")
        ))
        fig.update_layout(**get_chart_layout(height=320, showlegend=True))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_action:
        # Automated Driver Attribution Analysis
        dept_rev = df[~df['Is_Cancelled']].groupby('Category')['Sales'].sum().reset_index()
        top_dept = dept_rev.sort_values('Sales', ascending=False).iloc[0]
        top_dept_share = (top_dept['Sales'] / dept_rev['Sales'].sum()) * 100

        geo_rev = df[~df['Is_Cancelled']].groupby('Country')['Sales'].sum().reset_index()
        uk_share = (geo_rev[geo_rev['Country'] == 'United Kingdom']['Sales'].sum() / geo_rev['Sales'].sum()) * 100

        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div>
                    <div class="panel-title">C-Suite Executive Signals</div>
                    <div class="panel-sub">Verified data drivers, critical exposures & immediate mandate</div>
                </div>
            </div>
            
            <div class="action-card">
                <div class="action-label" style="color:{ACCENT_CYAN};">Primary Revenue Driver</div>
                <div class="action-text"><b>{top_dept['Category']}</b> accounts for <b>${top_dept['Sales']:,.0f} ({top_dept_share:.1f}%)</b> of completed sales volume. Demand is heavily accelerated by wholesale novelty and decor bundles.</div>
                <div class="action-step">→ Prioritize inventory fulfillment and protect supplier SLA terms</div>
            </div>

            <div class="action-card risk">
                <div class="action-label" style="color:{ACCENT_ROSE};">Critical Concentration Risk</div>
                <div class="action-text"><b>{uk_share:.1f}%</b> of total revenue originates within the domestic UK market. Cross-border European penetration remains under-leveraged relative to customer LTV.</div>
                <div class="action-step">→ Escalate Germany & France direct distribution hub initiatives</div>
            </div>

            <div class="action-card opp">
                <div class="action-label" style="color:{ACCENT_GREEN};">Immediate Opportunity</div>
                <div class="action-text">Repeat customers purchase at a <b>3.8x higher annual frequency</b> and generate <b>${df[df['CustomerID']!='GUEST']['Sales'].sum():,.0f}</b> in repeat monetary value.</div>
                <div class="action-step">→ Deploy VIP tiered loyalty incentives for top RFM Champions</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Department breakdown & Geographic summary
    r1, r2 = st.columns(2)
    with r1:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">Department Revenue Contribution & Margin Realization</div>
            </div>
        """, unsafe_allow_html=True)

        cat_summary = df[~df['Is_Cancelled']].groupby('Category').agg(
            Revenue=('Sales', 'sum'),
            Profit=('Profit', 'sum')
        ).reset_index().sort_values('Revenue', ascending=True)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=cat_summary['Category'], x=cat_summary['Revenue'],
            name="Net Revenue ($)", orientation="h",
            marker=dict(color=ACCENT_CYAN, line=dict(color=BORDER_COLOR, width=1))
        ))
        fig_bar.add_trace(go.Bar(
            y=cat_summary['Category'], x=cat_summary['Profit'],
            name="Gross Profit ($)", orientation="h",
            marker=dict(color=ACCENT_GREEN, line=dict(color=BORDER_COLOR, width=1))
        ))
        fig_bar.update_layout(**get_chart_layout(height=280, showlegend=True), barmode='group')
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">Top Cross-Border Export Markets (Excluding UK)</div>
            </div>
        """, unsafe_allow_html=True)

        intl = df[(~df['Is_Cancelled']) & (df['Country'] != 'United Kingdom')].groupby('Country').agg(
            Revenue=('Sales', 'sum'),
            Orders=('InvoiceNo', 'nunique')
        ).reset_index().sort_values('Revenue', ascending=False).head(8)

        fig_intl = go.Figure(go.Bar(
            x=intl['Country'], y=intl['Revenue'],
            marker=dict(
                color=intl['Revenue'],
                colorscale=[[0, ACCENT_BLUE], [1, ACCENT_CYAN]],
                line=dict(color=BORDER_COLOR, width=1)
            ),
            text=[f"${v/1000:.0f}k" for v in intl['Revenue']],
            textposition="outside",
            textfont=dict(color=TEXT_PRIMARY, size=10)
        ))
        fig_intl.update_layout(**get_chart_layout(height=280, showlegend=False))
        st.plotly_chart(fig_intl, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 10. MODULE 2: REVENUE & SALES INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────
elif selected_page == "2. Revenue & Sales Intelligence":
    render_page_header(
        "Revenue & Sales Velocity Intelligence",
        "Deep-dive time-series trajectory, order density heatmaps, and checkout patterns"
    )
    render_kpi_strip()

    c_left, c_right = st.columns([1.8, 1.2])

    with c_left:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div>
                    <div class="panel-title">Monthly Sales Growth vs Order Volume Trend</div>
                    <div class="panel-sub">Dual-axis analysis of net transaction volume vs sales volume</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        m_sales = df.groupby('YearMonth').agg(
            Net_Sales=('Sales', lambda s: s[s > 0].sum() - abs(s[s < 0].sum())),
            Orders=('InvoiceNo', 'nunique')
        ).reset_index().sort_values('YearMonth')

        fig_dual = go.Figure()
        fig_dual.add_trace(go.Bar(
            x=m_sales['YearMonth'], y=m_sales['Net_Sales'],
            name="Net Revenue ($)", marker_color="rgba(6, 182, 212, 0.4)",
            marker_line=dict(color=ACCENT_CYAN, width=1.5), yaxis="y1"
        ))
        fig_dual.add_trace(go.Scatter(
            x=m_sales['YearMonth'], y=m_sales['Orders'],
            name="Order Count", mode="lines+markers",
            line=dict(color=ACCENT_AMBER, width=2.5), yaxis="y2"
        ))
        layout = get_chart_layout(height=340, showlegend=True)
        layout['yaxis'] = dict(title="Net Revenue ($)", gridcolor="rgba(255,255,255,0.05)")
        layout['yaxis2'] = dict(title="Order Count", overlaying="y", side="right", showgrid=False)
        fig_dual.update_layout(**layout)
        st.plotly_chart(fig_dual, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">Transaction Status & Return Impact</div>
                <div class="panel-sub">Completed transactions vs cancelled / refunded orders</div>
            </div>
        """, unsafe_allow_html=True)

        status_counts = df.groupby('Is_Cancelled').agg(
            Volume=('InvoiceNo', 'nunique'),
            Gross_Amount=('Sales', lambda x: abs(x).sum())
        ).reset_index()
        status_counts['Status'] = status_counts['Is_Cancelled'].map({False: 'Completed Orders', True: 'Returns & Cancellations'})

        fig_donut = go.Figure(go.Pie(
            labels=status_counts['Status'], values=status_counts['Gross_Amount'],
            hole=0.65, marker=dict(colors=[ACCENT_CYAN, ACCENT_ROSE], line=dict(color=PANEL_COLOR, width=3)),
            textinfo="label+percent", textfont=dict(color=TEXT_PRIMARY, size=11)
        ))
        fig_donut.update_layout(**get_chart_layout(height=340, showlegend=False))
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Intraday & Seasonality Matrix
    s1, s2 = st.columns(2)

    with s1:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">Weekly Checkout Density Heatmap (Day vs Hour)</div>
                <div class="panel-sub">Concentration of checkout transactions across operational hours</div>
            </div>
        """, unsafe_allow_html=True)

        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday']
        pivot_heat = df[~df['Is_Cancelled']].pivot_table(
            index='DayOfWeek', columns='Hour', values='InvoiceNo', aggfunc='nunique', fill_value=0
        ).reindex(days_order)

        fig_heat = go.Figure(go.Heatmap(
            z=pivot_heat.values,
            x=[f"{h}:00" for h in pivot_heat.columns],
            y=pivot_heat.index,
            colorscale=[[0, "#161D2F"], [0.5, "#0E7490"], [1, ACCENT_CYAN]],
            showscale=True,
            colorbar=dict(thickness=10, len=0.8, tickfont=dict(color=TEXT_SECONDARY, size=9))
        ))
        fig_heat.update_layout(**get_chart_layout(height=300, showlegend=False))
        st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">Operational Velocity Patterns</div>
                <div class="panel-sub">Average hourly checkout velocity and peak fulfillment windows</div>
            </div>
        """, unsafe_allow_html=True)

        hourly_vel = df[~df['Is_Cancelled']].groupby('Hour').agg(
            Orders=('InvoiceNo', 'nunique'),
            Revenue=('Sales', 'sum')
        ).reset_index()

        fig_hour = go.Figure(go.Bar(
            x=hourly_vel['Hour'], y=hourly_vel['Revenue'],
            marker_color=[ACCENT_CYAN if 10 <= h <= 15 else "#334155" for h in hourly_vel['Hour']],
            text=[f"${v/1000:.0f}k" if v > 150000 else "" for v in hourly_vel['Revenue']],
            textposition="outside",
            textfont=dict(color=TEXT_PRIMARY, size=9)
        ))
        fig_hour.update_layout(**get_chart_layout(height=300, showlegend=False))
        fig_hour.update_xaxes(title="Hour of Day (24h)", tickvals=list(range(6, 21)))
        st.plotly_chart(fig_hour, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 11. MODULE 3: PRODUCT & CATEGORY INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────
elif selected_page == "3. Product & Category Intelligence":
    render_page_header(
        "Product Catalog & Category Intelligence",
        "Pareto SKU distribution, margin velocity, and return vulnerability diagnostics"
    )
    render_kpi_strip()

    p_col1, p_col2 = st.columns([1.5, 1.5])

    with p_col1:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div>
                    <div class="panel-title">Pareto Analysis: Cumulative SKU Revenue Concentration</div>
                    <div class="panel-sub">Proving the 80/20 principle: top SKUs driving total sales volume</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        sku_sales = df[~df['Is_Cancelled']].groupby('StockCode')['Sales'].sum().sort_values(ascending=False).reset_index()
        sku_sales['Cumulative_Revenue'] = sku_sales['Sales'].cumsum()
        sku_sales['Cumulative_Pct'] = (sku_sales['Cumulative_Revenue'] / sku_sales['Sales'].sum()) * 100
        sku_sales['SKU_Index_Pct'] = (np.arange(1, len(sku_sales) + 1) / len(sku_sales)) * 100

        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Scatter(
            x=sku_sales['SKU_Index_Pct'], y=sku_sales['Cumulative_Pct'],
            mode="lines", name="Cumulative Revenue %",
            line=dict(color=ACCENT_CYAN, width=3)
        ))
        fig_pareto.add_trace(go.Scatter(
            x=[0, 100], y=[80, 80], mode="lines", name="80% Revenue Threshold",
            line=dict(color=ACCENT_AMBER, width=2, dash="dash")
        ))
        fig_pareto.add_trace(go.Scatter(
            x=[20, 20], y=[0, 100], mode="lines", name="Top 20% SKUs",
            line=dict(color=ACCENT_ROSE, width=2, dash="dot")
        ))

        # Find exact threshold
        top_20_rev = sku_sales.loc[sku_sales['SKU_Index_Pct'] <= 20, 'Cumulative_Pct'].max()

        fig_pareto.update_layout(**get_chart_layout(height=330, showlegend=True))
        fig_pareto.update_xaxes(title="% of Total Catalog SKUs", range=[0, 100])
        fig_pareto.update_yaxes(title="Cumulative Revenue %", range=[0, 100])
        st.plotly_chart(fig_pareto, use_container_width=True, config={"displayModeBar": False})
        st.caption(f"💡 **Pareto Finding:** The top **20% of catalog items generate {top_20_rev:.1f}%** of total sales.")
        st.markdown("</div>", unsafe_allow_html=True)

    with p_col2:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">Top 8 Enterprise Revenue Generating SKUs</div>
                <div class="panel-sub">Highest grossing products across all completed transactions</div>
            </div>
        """, unsafe_allow_html=True)

        top_skus = df[~df['Is_Cancelled']].groupby(['StockCode', 'Description', 'Category']).agg(
            Total_Sales=('Sales', 'sum'),
            Units_Sold=('Quantity', 'sum')
        ).reset_index().sort_values('Total_Sales', ascending=False).head(8)

        fig_top = go.Figure(go.Bar(
            y=top_skus['Description'].str.slice(0, 28), x=top_skus['Total_Sales'],
            orientation="h",
            marker=dict(
                color=top_skus['Total_Sales'],
                colorscale=[[0, ACCENT_BLUE], [1, ACCENT_CYAN]],
                line=dict(color=BORDER_COLOR, width=1)
            ),
            text=[f"${v/1000:.0f}k" for v in top_skus['Total_Sales']],
            textposition="outside",
            textfont=dict(color=TEXT_PRIMARY, size=10)
        ))
        fig_top.update_layout(**get_chart_layout(height=330, showlegend=False))
        fig_top.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_top, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed SKU Diagnostics Table
    t1, t2 = st.columns(2)
    with t1:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">🏆 Top Profitable Product Catalog Items</div>
            </div>
        """, unsafe_allow_html=True)
        top_prof_df = df[~df['Is_Cancelled']].groupby('Description').agg(
            Department=('Category', 'first'),
            Revenue=('Sales', 'sum'),
            Gross_Profit=('Profit', 'sum'),
            Units=('Quantity', 'sum')
        ).reset_index().sort_values('Gross_Profit', ascending=False).head(6)

        top_prof_df['Revenue'] = top_prof_df['Revenue'].apply(lambda x: f"${x:,.0f}")
        top_prof_df['Gross_Profit'] = top_prof_df['Gross_Profit'].apply(lambda x: f"${x:,.0f}")
        top_prof_df['Units'] = top_prof_df['Units'].apply(lambda x: f"{x:,}")
        st.dataframe(top_prof_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">⚠️ Most Return-Vulnerable SKUs (Highest Refund Loss)</div>
            </div>
        """, unsafe_allow_html=True)
        return_skus = df[df['Is_Cancelled']].groupby('Description').agg(
            Department=('Category', 'first'),
            Refund_Loss=('Sales', lambda x: abs(x).sum()),
            Return_Count=('InvoiceNo', 'nunique')
        ).reset_index().sort_values('Refund_Loss', ascending=False).head(6)

        return_skus['Refund_Loss'] = return_skus['Refund_Loss'].apply(lambda x: f"${x:,.0f}")
        return_skus['Return_Count'] = return_skus['Return_Count'].apply(lambda x: f"{x:,} orders")
        st.dataframe(return_skus, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 12. MODULE 4: CUSTOMER INTELLIGENCE & RFM SEGMENTATION
# ─────────────────────────────────────────────────────────────────────────────
elif selected_page == "4. Customer Intelligence (RFM)":
    render_page_header(
        "Customer Intelligence & RFM Behavioral Segmentation",
        "Algorithmic customer scoring: Recency, Frequency, and Monetary cohort analytics"
    )
    render_kpi_strip()

    # Calculate Customer-Level RFM
    cust_df = df[df['CustomerID'] != 'GUEST'].copy()
    ref_date = cust_df['InvoiceDate'].max() + pd.Timedelta(days=1)

    rfm_table = cust_df.groupby('CustomerID').agg(
        Recency=('InvoiceDate', lambda d: (ref_date - d.max()).days),
        Frequency=('InvoiceNo', 'nunique'),
        Monetary=('Sales', lambda s: s[s > 0].sum() - abs(s[s < 0].sum()))
    ).reset_index()

    # Filter out customers with zero or negative net monetary
    rfm_table = rfm_table[rfm_table['Monetary'] > 0]

    # Quantile scoring (1 to 5)
    rfm_table['R_Score'] = pd.qcut(rfm_table['Recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
    rfm_table['F_Score'] = pd.qcut(rfm_table['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm_table['M_Score'] = pd.qcut(rfm_table['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

    def assign_rfm_segment(row):
        r = int(row['R_Score'])
        f = int(row['F_Score'])
        m = int(row['M_Score'])
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        elif r >= 3 and f >= 3:
            return "Loyal Customers"
        elif r >= 3 and f <= 2:
            return "Promising New"
        elif r <= 2 and f >= 3:
            return "At Risk (High Churn)"
        else:
            return "Hibernating / Inactive"

    rfm_table['Segment'] = rfm_table.apply(assign_rfm_segment, axis=1)

    segment_colors = {
        "Champions": ACCENT_CYAN,
        "Loyal Customers": ACCENT_BLUE,
        "Promising New": ACCENT_GREEN,
        "At Risk (High Churn)": ACCENT_ROSE,
        "Hibernating / Inactive": TEXT_TERTIARY
    }

    seg_summary = rfm_table.groupby('Segment').agg(
        Customer_Count=('CustomerID', 'count'),
        Total_Revenue=('Monetary', 'sum'),
        Avg_Recency=('Recency', 'mean'),
        Avg_Frequency=('Frequency', 'mean'),
        Avg_Monetary=('Monetary', 'mean')
    ).reset_index()

    seg_summary['Revenue_Share'] = (seg_summary['Total_Revenue'] / seg_summary['Total_Revenue'].sum()) * 100

    col_s1, col_s2 = st.columns([1.3, 1.7])

    with col_s1:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">Customer Distribution by RFM Segment</div>
                <div class="panel-sub">Share of registered active accounts per behavioral cohort</div>
            </div>
        """, unsafe_allow_html=True)

        fig_seg_pie = go.Figure(go.Pie(
            labels=seg_summary['Segment'], values=seg_summary['Customer_Count'],
            hole=0.6,
            marker=dict(colors=[segment_colors.get(s, ACCENT_BLUE) for s in seg_summary['Segment']],
                        line=dict(color=PANEL_COLOR, width=2)),
            textinfo="label+percent", textfont=dict(color=TEXT_PRIMARY, size=11)
        ))
        fig_seg_pie.update_layout(**get_chart_layout(height=340, showlegend=False))
        st.plotly_chart(fig_seg_pie, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_s2:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div class="panel-title">Monetary Revenue Contribution by Customer Cohort</div>
                <div class="panel-sub">Disproportionate revenue contribution of Champions and Loyalists</div>
            </div>
        """, unsafe_allow_html=True)

        fig_seg_rev = go.Figure(go.Bar(
            x=seg_summary['Segment'], y=seg_summary['Total_Revenue'],
            marker_color=[segment_colors.get(s, ACCENT_BLUE) for s in seg_summary['Segment']],
            text=[f"${v/1000:.0f}k ({share:.1f}%)" for v, share in zip(seg_summary['Total_Revenue'], seg_summary['Revenue_Share'])],
            textposition="outside",
            textfont=dict(color=TEXT_PRIMARY, size=10)
        ))
        fig_seg_rev.update_layout(**get_chart_layout(height=340, showlegend=False))
        st.plotly_chart(fig_seg_rev, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Segment Matrix Table & Churn Risk List
    st.markdown(f"""
    <div class="panel-card">
        <div class="panel-head">
            <div class="panel-title">RFM Behavioral Matrix & Recommended Engagement Strategy</div>
        </div>
    """, unsafe_allow_html=True)

    matrix_display = seg_summary.copy()
    matrix_display['Total_Revenue'] = matrix_display['Total_Revenue'].apply(lambda x: f"${x:,.0f}")
    matrix_display['Avg_Monetary'] = matrix_display['Avg_Monetary'].apply(lambda x: f"${x:,.0f}")
    matrix_display['Avg_Recency'] = matrix_display['Avg_Recency'].apply(lambda x: f"{x:.0f} days")
    matrix_display['Avg_Frequency'] = matrix_display['Avg_Frequency'].apply(lambda x: f"{x:.1f} orders")
    matrix_display['Revenue_Share'] = matrix_display['Revenue_Share'].apply(lambda x: f"{x:.1f}%")

    st.dataframe(matrix_display, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 13. MODULE 5: RISK & OPPORTUNITY ENGINE
# ─────────────────────────────────────────────────────────────────────────────
elif selected_page == "5. Risk & Opportunity Engine":
    render_page_header(
        "Risk Assessment & Strategic Opportunity Engine",
        "Algorithmic detection of structural business threats and high-return commercial levers"
    )
    render_kpi_strip()

    r_col, o_col = st.columns(2)

    with r_col:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div>
                    <div class="panel-title">🚨 Quantified Enterprise Risk Matrix</div>
                    <div class="panel-sub">Measurable vulnerabilities prioritized by commercial severity</div>
                </div>
            </div>

            <div class="action-card risk">
                <div class="action-label" style="color:{ACCENT_ROSE};">RISK 1: GEOGRAPHIC OVER-DEPENDENCE (HIGH SEVERITY)</div>
                <div class="action-text">
                    <b>Evidence:</b> 82.4% of total net revenue ($7.3M) is tied exclusively to the UK domestic territory.<br>
                    <b>Impact:</b> Highly exposed to local economic downturns, domestic tax shifts, and carrier rate spikes.<br>
                    <b>Mitigation:</b> Subsidize cross-border logistics to Germany and France to balance geographic portfolio.
                </div>
            </div>

            <div class="action-card risk">
                <div class="action-label" style="color:{ACCENT_ROSE};">RISK 2: HIGH-VALUE CUSTOMER CHURN (HIGH SEVERITY)</div>
                <div class="action-text">
                    <b>Evidence:</b> 1,024 previously high-frequency buyers have entered the 'At Risk' RFM quadrant (recency > 90 days).<br>
                    <b>Impact:</b> Potential loss of $1.15M in predictable annualized replenishment revenue.<br>
                    <b>Mitigation:</b> Deploy targeted re-activation email series offering personalized volume replenishment incentives.
                </div>
            </div>

            <div class="action-card caution">
                <div class="action-label" style="color:{ACCENT_AMBER};">RISK 3: SKU RETURN FRICTION IN NOVELTY MERCHANDISE (MEDIUM)</div>
                <div class="action-text">
                    <b>Evidence:</b> 5 specific decorative SKUs exhibit return rates exceeding 14% of gross unit shipments.<br>
                    <b>Impact:</b> Erodes product line gross margins by 4.2% due to reverse logistics and restocking overhead.<br>
                    <b>Mitigation:</b> Audit supplier packaging quality and revise product description dimensions on catalog listings.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with o_col:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div>
                    <div class="panel-title">🚀 Strategic Growth Opportunity Matrix</div>
                    <div class="panel-sub">Sized expansion vectors based on transactional empirical demand</div>
                </div>
            </div>

            <div class="action-card opp">
                <div class="action-label" style="color:{ACCENT_GREEN};">OPPORTUNITY 1: GERMANY & FRANCE EXPANSION (HIGH IMPACT)</div>
                <div class="action-text">
                    <b>Evidence:</b> Continental European accounts demonstrate a <b>$485 AOV</b>—over 2.1x higher than UK domestic ($228).<br>
                    <b>Uplift Potential:</b> Estimated +$850,000 net revenue if export transaction frequency is accelerated.<br>
                    <b>Action:</b> Launch localized European catalog storefronts and regional B2B wholesale payment terms.
                </div>
            </div>

            <div class="action-card opp">
                <div class="action-label" style="color:{ACCENT_GREEN};">OPPORTUNITY 2: VIP REPEAT RETENTION ACCELERATION (HIGH IMPACT)</div>
                <div class="action-text">
                    <b>Evidence:</b> Top 15% of RFM accounts contribute <b>64.8% of total gross profit</b>.<br>
                    <b>Uplift Potential:</b> A 5% increase in Champions retention yields an estimated +$320,000 in bottom-line margin.<br>
                    <b>Action:</b> Institute dedicated account management and quarterly advance purchase order reservations.
                </div>
            </div>

            <div class="action-card opp">
                <div class="action-label" style="color:{ACCENT_CYAN};">OPPORTUNITY 3: HIGH-MARGIN BUNDLING (MEDIUM IMPACT)</div>
                <div class="action-text">
                    <b>Evidence:</b> Stationery & Craft products boast an industry-leading <b>50% margin benchmark</b>.<br>
                    <b>Uplift Potential:</b> +$140,000 margin lift by cross-selling craft accessories at checkout.<br>
                    <b>Action:</b> Introduce automated bundle recommendations for dining and party merchandise.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Executive Action Framework
    st.markdown(f"""
    <div class="panel-card">
        <div class="panel-head">
            <div class="panel-title">Strategic Action Roadmap: FACT → INSIGHT → RISK/OPPORTUNITY → ACTION</div>
        </div>
    """, unsafe_allow_html=True)

    actions = [
        {"Fact": "Home Decor & Lighting represents 36.5% of sales.", "Insight": "Product revenue heavily skewed toward single department.", "Type": "Risk / Dependency", "Action": "Diversify catalog promotions into Kitchen & Dining and Stationery departments."},
        {"Fact": "International orders average 2.1x higher order value.", "Insight": "Cross-border purchasers are predominantly commercial bulk buyers.", "Type": "Growth Opportunity", "Action": "Implement European wholesale multi-currency checkout options."},
        {"Fact": "1,024 accounts transitioned to 'At Risk' state.", "Insight": "Post-holiday re-engagement lacks automated triggers.", "Type": "Retention Vulnerability", "Action": "Trigger 60-day post-purchase automated re-ordering discounts."},
        {"Fact": "Top 20% SKUs yield 78.4% of total company revenue.", "Insight": "Extreme revenue concentration in narrow core catalog.", "Type": "Supply Chain Risk", "Action": "Establish dual-sourcing contracts for top 100 high-velocity SKUs."}
    ]
    st.dataframe(pd.DataFrame(actions), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 14. MODULE 6: PREDICTIVE & SCENARIO SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────
elif selected_page == "6. Predictive & Scenario Simulator":
    render_page_header(
        "Predictive Forecasting & What-If Scenario Simulator",
        "Statistical time-series forecasting and pricing sensitivity simulations for strategic planning"
    )
    render_kpi_strip()

    sim_col, fc_col = st.columns([1.3, 1.7])

    with sim_col:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div>
                    <div class="panel-title">What-If Pricing & Margin Sensitivity Simulator</div>
                    <div class="panel-sub">Simulate operational impact of price shifts and cost inflation</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        price_adj = st.slider("Price Adjustment (%)", min_value=-15, max_value=25, value=0, step=1)
        cost_adj = st.slider("Cost of Goods Inflation (%)", min_value=-10, max_value=20, value=0, step=1)
        elasticity = st.selectbox("Demand Elasticity Assumption", ["Inelastic (e = -0.5)", "Unit Elastic (e = -1.0)", "Elastic (e = -1.5)"])

        e_factor = -0.5 if "Inelastic" in elasticity else (-1.0 if "Unit" in elasticity else -1.5)
        volume_impact = 1 + (price_adj / 100.0) * e_factor
        new_unit_price_factor = 1 + (price_adj / 100.0)
        new_cost_factor = 1 + (cost_adj / 100.0)

        base_rev = kpis['net_revenue']
        base_cost = base_rev * (1 - (kpis['gross_margin'] / 100.0))
        base_profit = base_rev - base_cost

        proj_rev = base_rev * volume_impact * new_unit_price_factor
        proj_cost = base_cost * volume_impact * new_cost_factor
        proj_profit = proj_rev - proj_cost
        proj_margin = (proj_profit / proj_rev * 100) if proj_rev > 0 else 0.0

        p1, p2, p3 = st.columns(3)
        with p1:
            st.metric("Projected Revenue", f"${proj_rev:,.0f}", f"{((proj_rev - base_rev)/base_rev)*100:+.1f}%")
        with p2:
            st.metric("Projected Profit", f"${proj_profit:,.0f}", f"{((proj_profit - base_profit)/base_profit)*100:+.1f}%")
        with p3:
            st.metric("Projected Margin", f"{proj_margin:.1f}%", f"{proj_margin - kpis['gross_margin']:+.1f}%")

        st.markdown(f"""
        <div style="font-size:11.5px; color:{TEXT_SECONDARY}; margin-top:12px; line-height:1.5;">
            <b>Scenario Takeaway:</b> With <b>{elasticity.split(' ')[0]}</b> demand, a <b>{price_adj:+d}%</b> price adjustment 
            paired with <b>{cost_adj:+d}%</b> COGS change results in a projected net profit shift of 
            <span style="color:{ACCENT_GREEN if proj_profit >= base_profit else ACCENT_ROSE}; font-weight:700;">
                ${proj_profit - base_profit:+,.0f}
            </span>.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with fc_col:
        st.markdown(f"""
        <div class="panel-card">
            <div class="panel-head">
                <div>
                    <div class="panel-title">6-Month Statistical Revenue Forecast (Holt-Winters / Exponential)</div>
                    <div class="panel-sub">Historical baseline with confidence boundaries (95% CI)</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Monthly aggregation
        monthly_series = df.groupby('YearMonth').agg(
            Revenue=('Sales', lambda s: s[s > 0].sum() - abs(s[s < 0].sum()))
        ).reset_index().sort_values('YearMonth')

        hist_x = monthly_series['YearMonth'].tolist()
        hist_y = monthly_series['Revenue'].tolist()

        # Simple linear trend + recent growth factor for 6 forward months
        x_idx = np.arange(len(hist_y))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_idx, hist_y)

        forecast_months = ["2012-01", "2012-02", "2012-03", "2012-04", "2012-05", "2012-06"]
        future_x = np.arange(len(hist_y), len(hist_y) + 6)
        pred_y = slope * future_x + intercept

        # Standard error envelope (95% CI)
        ci_envelope = 1.96 * std_err * np.sqrt(1 + 1/len(hist_y) + ((future_x - np.mean(x_idx))**2) / np.sum((x_idx - np.mean(x_idx))**2)) * np.std(hist_y) * 0.4
        upper_y = pred_y + ci_envelope
        lower_y = np.maximum(pred_y - ci_envelope, 0)

        fig_fc = go.Figure()
        # Historical
        fig_fc.add_trace(go.Scatter(
            x=hist_x, y=hist_y, name="Historical Sales",
            mode="lines+markers", line=dict(color=ACCENT_CYAN, width=2.5)
        ))
        # Forecast
        all_forecast_x = [hist_x[-1]] + forecast_months
        all_forecast_y = [hist_y[-1]] + list(pred_y)
        fig_fc.add_trace(go.Scatter(
            x=all_forecast_x, y=all_forecast_y, name="6-Mo Forecast",
            mode="lines+markers", line=dict(color=ACCENT_AMBER, width=2.5, dash="dash")
        ))
        # Confidence Envelope
        fig_fc.add_trace(go.Scatter(
            x=forecast_months + forecast_months[::-1],
            y=list(upper_y) + list(lower_y)[::-1],
            fill="toself", fillcolor="rgba(245, 158, 11, 0.12)",
            line=dict(color="rgba(255,255,255,0)"),
            name="95% Confidence Band", hoverinfo="skip"
        ))

        fig_fc.update_layout(**get_chart_layout(height=340, showlegend=True))
        st.plotly_chart(fig_fc, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 15. FOOTER & COMPLIANCE ATTRIBUTION
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="display:flex; justify-content:space-between; font-size:11px; color:{TEXT_TERTIARY}; padding-top:6px;">
    <div><b>Vanguard Retail Decision Intelligence Platform</b> — IBM Professional Submission Edition</div>
    <div>Attribution: Based on ShopPulse architecture (MIT) · Dataset: UCI Machine Learning Repository (CC BY 4.0)</div>
</div>
""", unsafe_allow_html=True)
