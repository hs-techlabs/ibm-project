import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from analytics import ShopPulseAnalytics

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ShopPulse — E-commerce BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Design tokens — authentic Power BI / Fluent look
# ─────────────────────────────────────────────
BG          = "#F3F2F1"   # report canvas — PBI's default gray canvas
PANEL       = "#FFFFFF"   # sidebar
CARD        = "#FFFFFF"   # visual card
BORDER      = "#E1DFDD"   # Fluent hairline
BORDER_STR  = "#C8C6C4"
TEXT        = "#252423"   # Fluent neutral primary
TEXT_MUTE   = "#605E5C"   # Fluent neutral secondary
TEXT_FAINT  = "#A19F9D"   # Fluent neutral tertiary
ACCENT      = "#01B8AA"   # Power BI default primary (teal)
ACCENT_2    = "#374649"   # PBI secondary (slate)
POS         = "#107C10"   # Fluent success green
NEG         = "#D13438"   # Fluent danger red
WARN        = "#F2C80F"   # PBI palette yellow

# Power BI's actual default report color palette
PALETTE = ["#01B8AA", "#374649", "#FD625E", "#F2C80F", "#5F6B6D", "#8AD4EB", "#FE9666", "#A66999", "#3599B8"]

KPI_ACCENTS = {
    "revenue": "#01B8AA", "orders": "#3599B8", "aov": "#FE9666", "growth": POS, "units": "#A66999"
}

# ─────────────────────────────────────────────
# Global CSS — enterprise BI look
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp {{
    background-color: {BG} !important;
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif !important;
}}
header[data-testid="stHeader"] {{ background-color: {BG} !important; }}
#MainMenu, footer, .stDeployButton {{ display: none !important; }}
.block-container {{ padding-top: 0.9rem !important; padding-bottom: 2rem !important; max-width: 1560px; }}

/* ── Sidebar / nav rail (Fluent light) ── */
section[data-testid="stSidebar"] {{
    background-color: {PANEL} !important;
    border-right: 1px solid {BORDER};
    width: 250px !important;
    box-shadow: 1px 0 3px rgba(0,0,0,0.04);
}}
section[data-testid="stSidebar"] > div {{ padding-top: 0.6rem; }}
.brand {{
    display:flex; align-items:center; gap:10px; padding: 6px 4px 16px 4px;
    border-bottom: 1px solid {BORDER}; margin-bottom: 14px;
}}
.brand-badge {{
    width: 32px; height: 32px; border-radius: 6px;
    background: {ACCENT};
    display:flex; align-items:center; justify-content:center;
    font-weight:700; color:#fff; font-size:14px;
}}
.brand-title {{ font-size: 15px; font-weight: 700; color: {TEXT}; line-height:1.1; }}
.brand-sub {{ font-size: 10.5px; color: {TEXT_FAINT}; letter-spacing: 0.3px; }}

.nav-label {{ font-size: 10.5px; color: {TEXT_FAINT}; text-transform: uppercase; letter-spacing: 0.8px; font-weight:700; margin: 4px 0 6px 6px; }}

section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {{ gap: 1px; }}
section[data-testid="stSidebar"] .stRadio label {{
    padding: 8px 10px !important; border-radius: 4px !important;
    border-left: 3px solid transparent; margin-bottom: 0px;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{ background: #F3F2F1; }}
section[data-testid="stSidebar"] .stRadio label:has(input:checked) {{
    background: #E9F9F7 !important; border-left: 3px solid {ACCENT} !important;
}}
section[data-testid="stSidebar"] .stRadio label:has(input:checked) span {{ color: {ACCENT_2} !important; font-weight: 600 !important; }}
section[data-testid="stSidebar"] .stRadio label span {{ color: {TEXT_MUTE} !important; font-size: 13.5px !important; }}
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {{ display:none; }}

section[data-testid="stSidebar"] .stSelectbox label, section[data-testid="stSidebar"] .stRadio > label {{
    color: {TEXT_FAINT} !important; font-size: 10.5px !important; text-transform: uppercase; letter-spacing: 0.7px; font-weight: 700 !important;
}}
section[data-testid="stSidebar"] hr {{ border-color: {BORDER}; margin: 14px 0; }}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background: #fff !important; border: 1px solid {BORDER_STR} !important; border-radius: 4px !important;
}}
section[data-testid="stSidebar"] div[data-baseweb="select"] span {{ color: {TEXT} !important; }}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6 {{ color: {TEXT} !important; font-family:'Segoe UI','Inter',sans-serif !important; }}
.stMarkdown p, .stCaption, label {{ color: {TEXT_MUTE} !important; }}

/* ── Page header ── */
.page-head {{ display:flex; align-items:baseline; justify-content:space-between; margin-bottom: 12px;
    padding-bottom: 10px; border-bottom: 1px solid {BORDER}; }}
.page-title {{ font-size: 20px; font-weight: 700; color: {TEXT}; letter-spacing: -0.2px; }}
.page-meta {{ font-size: 11.5px; color: {TEXT_FAINT}; background: #fff; border: 1px solid {BORDER}; padding: 3px 10px; border-radius: 4px; }}

/* ── KPI cards ── */
.kpi-card {{
    background: {CARD}; border: 1px solid {BORDER}; border-top: 3px solid var(--kc, {ACCENT});
    border-radius: 6px; padding: 13px 15px 9px 15px; height: 100%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
.kpi-label {{ font-size: 10.5px; font-weight: 600; color: {TEXT_MUTE}; text-transform: uppercase; letter-spacing: 0.5px; }}
.kpi-value {{ font-size: 24px; font-weight: 700; color: {TEXT}; margin: 4px 0 6px 0; letter-spacing: -0.3px; font-family:'Segoe UI',sans-serif; }}
.kpi-delta {{ display:inline-flex; align-items:center; gap:3px; font-size: 11.5px; font-weight: 700; padding: 2px 7px; border-radius: 4px; }}
.kpi-delta.pos {{ color: {POS}; background: #DFF6DD; }}
.kpi-delta.neg {{ color: {NEG}; background: #FDE7E9; }}
.kpi-delta.flat {{ color: {TEXT_FAINT}; background: #F3F2F1; }}

/* ── Panel / chart card ── */
.panel {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 6px;
    padding: 15px 17px 10px 17px; margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
.panel-head {{ display:flex; align-items:center; justify-content:space-between; margin-bottom: 10px;
    padding-bottom: 8px; border-bottom: 1px solid #F3F2F1; }}
.panel-title {{ font-size: 13px; font-weight: 600; color: {TEXT}; letter-spacing: 0.05px; }}
.panel-sub {{ font-size: 11px; color: {TEXT_FAINT}; margin-top: 1px; }}

/* ── Signal cards ── */
.signal {{ border-radius: 4px; padding: 10px 12px; margin-bottom: 8px; background: #FAFAF9; border-left: 3px solid {ACCENT}; }}
.signal.spike   {{ border-left-color: {POS}; }}
.signal.abandon {{ border-left-color: {NEG}; }}
.signal.restock {{ border-left-color: #3599B8; }}
.signal.margin  {{ border-left-color: #F2C80F; }}
.signal-t {{ font-weight: 600; font-size: 12.5px; color: {TEXT}; margin-bottom: 2px; }}
.signal-m {{ font-size: 11.5px; color: {TEXT_MUTE}; line-height: 1.5; }}

/* ── RFM rows ── */
.rfm-row {{ display:flex; align-items:center; justify-content:space-between; padding: 9px 4px; border-bottom: 1px solid #F3F2F1; }}
.rfm-row:last-child {{ border-bottom: none; }}
.rfm-dot {{ width: 9px; height: 9px; border-radius: 50%; display:inline-block; margin-right: 9px; }}
.rfm-name {{ font-size: 13px; font-weight: 600; color: {TEXT}; }}
.rfm-desc {{ font-size: 10.5px; color: {TEXT_FAINT}; margin-left: 18px; }}
.rfm-count {{ font-size: 12.5px; font-weight: 700; padding: 3px 10px; border-radius: 4px; }}

/* ── What-if boxes ── */
.wif {{ background: #F5FCFB; border: 1px solid {BORDER}; border-radius: 5px; padding: 12px; text-align:center; }}
.wif span {{ font-size: 10.5px; color: {TEXT_FAINT}; text-transform:uppercase; letter-spacing:0.5px; }}
.wif h4 {{ font-size: 18px; font-weight: 700; color: {TEXT} !important; margin: 5px 0 0 0 !important; }}

/* ── Records table (custom HTML) ── */
.rec-table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; }}
.rec-table th {{ text-align:left; color: {TEXT_FAINT}; font-weight:600; font-size:10.5px; text-transform:uppercase;
    letter-spacing:0.4px; padding: 7px 10px; border-bottom: 2px solid {BORDER}; background: #FAFAF9; }}
.rec-table td {{ padding: 8px 10px; color: {TEXT_MUTE}; border-bottom: 1px solid #F3F2F1; }}
.rec-table tr:hover td {{ background: #FAFAF9; }}
.pill {{ display:inline-block; padding: 2px 9px; border-radius: 4px; font-size: 10px; font-weight: 700; }}
.pill-completed, .pill-delivered, .pill-shipped {{ background: #DFF6DD; color: {POS}; }}
.pill-pending    {{ background: #FFF4CE; color: #8A6D00; }}
.pill-cancelled  {{ background: #FDE7E9; color: {NEG}; }}
.pill-default    {{ background: #F3F2F1; color: {TEXT_MUTE}; }}

/* ── Streamlit table (fallback pages) ── */
div[data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 6px; }}
div[data-testid="stDataFrame"] th {{ background-color: #FAFAF9 !important; color: {TEXT_MUTE} !important; }}
div[data-testid="stDataFrame"] td {{ color: {TEXT_MUTE} !important; }}

/* ── Chat ── */
.chat-ai   {{ background: #FAFAF9; border: 1px solid {BORDER}; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; color: {TEXT_MUTE}; font-size: 13px; line-height: 1.6; }}
.chat-user {{ background: {ACCENT}; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; color: #fff; font-size: 13px; line-height: 1.6; text-align: right; }}

/* ── Slider / misc widget accents ── */
.stSlider [data-baseweb="slider"] > div > div {{ background: {ACCENT} !important; }}
.stDownloadButton > button {{
    background: {ACCENT} !important; color: #fff !important; font-weight: 600 !important;
    border: none !important; border-radius: 4px !important; font-size: 12.5px !important;
}}
.stPlotlyChart {{ border-radius: 4px; }}
[data-testid="stMetricValue"] {{ color: {TEXT} !important; }}
[data-testid="stMetricLabel"] {{ color: {TEXT_MUTE} !important; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Data engine
# ─────────────────────────────────────────────
@st.cache_resource
def load_analytics():
    return ShopPulseAnalytics()

analytics = load_analytics()

# ─────────────────────────────────────────────
# Plotly base template
# ─────────────────────────────────────────────
def plot_layout(height=320, showlegend=False):
    return dict(
        height=height,
        paper_bgcolor=CARD, plot_bgcolor=CARD,
        font=dict(family="Segoe UI, Inter, sans-serif", color=TEXT_MUTE, size=11.5),
        margin=dict(l=6, r=6, t=6, b=6),
        showlegend=showlegend,
        legend=dict(orientation="h", y=1.16, x=0, font=dict(color=TEXT_MUTE, size=11)),
        xaxis=dict(gridcolor="#F3F2F1", zerolinecolor="#E1DFDD", linecolor=BORDER_STR),
        yaxis=dict(gridcolor="#F3F2F1", zerolinecolor="#E1DFDD", linecolor=BORDER_STR),
        hoverlabel=dict(bgcolor="#252423", font_color="#fff", bordercolor=BORDER),
    )

def hex_to_rgba(hex_color, alpha=0.13):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def panel_open(title, subtitle=None):
    sub = f'<div class="panel-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""<div class="panel"><div class="panel-head"><div><div class="panel-title">{title}</div>{sub}</div></div>""", unsafe_allow_html=True)

def panel_close():
    st.markdown("</div>", unsafe_allow_html=True)

def kpi_card(container, label, value, delta=None, accent=ACCENT, spark=None):
    with container:
        cls, arrow = "flat", "→"
        if delta is not None:
            cls = "pos" if delta > 0 else ("neg" if delta < 0 else "flat")
            arrow = "▲" if delta > 0 else ("▼" if delta < 0 else "→")
        delta_html = f'<span class="kpi-delta {cls}">{arrow} {abs(delta):.1f}%</span>' if delta is not None else ""
        st.markdown(f"""
        <div class="kpi-card" style="--kc:{accent};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)
        if spark is not None and len(spark) > 1:
            fig = go.Figure(go.Scatter(y=spark, mode="lines", line=dict(color=accent, width=2), fill="tozeroy", fillcolor=hex_to_rgba(accent, 0.15)))
            fig.update_layout(height=42, margin=dict(l=0, r=0, t=2, b=0), paper_bgcolor=CARD, plot_bgcolor=CARD,
                               xaxis=dict(visible=False), yaxis=dict(visible=False), showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ─────────────────────────────────────────────
# Sidebar — brand + nav + filters
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-badge">SP</div>
        <div>
            <div class="brand-title">ShopPulse</div>
            <div class="brand-sub">E-commerce BI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Reports</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["🏠 Overview", "📈 Sales", "📦 Product", "👥 Customer", "🌍 Regional", "💰 Profitability", "🤖 AI Assistant"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div class="nav-label">Filters</div>', unsafe_allow_html=True)
    categories = ["All"] + sorted(analytics.merged["Category"].dropna().unique().tolist())
    selected_cat = st.selectbox("Category", categories, index=0, label_visibility="visible")
    timeframe = st.radio("Time Period", ["YTD", "YoY", "All Time"], horizontal=True)
    tf_map = {"YTD": "YTD", "YoY": "YoY", "All Time": None}

    st.markdown("---")
    kpi_data = analytics.get_kpis(category=selected_cat, timeframe=tf_map[timeframe])
    csv_report = pd.DataFrame([kpi_data]).to_csv(index=False)
    st.download_button("⬇  Download Report", csv_report, "ShopPulse_Report.csv", "text/csv", use_container_width=True)


# ─────────────────────────────────────────────
# Shared data for header + KPI strip
# ─────────────────────────────────────────────
kpis = analytics.get_kpis(category=selected_cat, timeframe=tf_map[timeframe])
trends = analytics.get_revenue_trends(category=selected_cat, timeframe=tf_map[timeframe])

page_titles = {
    "🏠 Overview": ("Executive Overview", "Company-wide performance at a glance"),
    "📈 Sales": ("Sales Intelligence", "Trends, funnel and daily patterns"),
    "📦 Product": ("Product Intelligence", "Category and profitability breakdown"),
    "👥 Customer": ("Customer Intelligence", "RFM segmentation"),
    "🌍 Regional": ("Regional Intelligence", "Performance by state"),
    "💰 Profitability": ("Profitability & Forecast", "Scenario simulation and revenue outlook"),
    "🤖 AI Assistant": ("AI Analytics Assistant", "Ask questions in plain language"),
}
title, subtitle = page_titles[page]
st.markdown(f"""
<div class="page-head">
    <div class="page-title">{title}</div>
    <div class="page-meta">Filter: {selected_cat} &nbsp;·&nbsp; {timeframe}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  KPI Strip — every page
# ══════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
kpi_card(k1, "Total Revenue", f"${kpis['total_revenue']:,.0f}", kpis['growth_rate'], KPI_ACCENTS["revenue"], spark=trends.get("revenue"))
kpi_card(k2, "Total Orders", f"{kpis['total_orders']:,}", kpis['order_growth'], KPI_ACCENTS["orders"], spark=trends.get("profit"))
kpi_card(k3, "Avg Order Value", f"${kpis['aov']:,.2f}", None, KPI_ACCENTS["aov"])
kpi_card(k4, "Growth Rate", f"{kpis['growth_rate']:.1f}%", kpis['growth_rate'], KPI_ACCENTS["growth"])
kpi_card(k5, "Units Sold", f"{kpis['units_sold']:,}", None, KPI_ACCENTS["units"])

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  PAGE: Overview / Sales
# ══════════════════════════════════════════════
if page in ["🏠 Overview", "📈 Sales"]:

    col_main, col_right = st.columns([2, 1])

    with col_main:
        panel_open("Revenue &amp; Profit Trend", "Monthly, current filter")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trends["labels"], y=trends["revenue"], mode="lines", name="Revenue",
                                  line=dict(color=ACCENT, width=2.5, shape="spline"), fill="tozeroy", fillcolor=hex_to_rgba(ACCENT, 0.10)))
        fig.add_trace(go.Scatter(x=trends["labels"], y=trends["profit"], mode="lines", name="Profit",
                                  line=dict(color=ACCENT_2, width=2, dash="dot", shape="spline")))
        fig.update_layout(**plot_layout(height=330, showlegend=True))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    with col_right:
        panel_open("Sales Signals", "Auto-detected this period")
        signals = analytics.get_sales_signals()
        signal_classes = ["spike", "abandon", "restock", "margin"]
        for i, sig in enumerate(signals):
            cls = signal_classes[i % len(signal_classes)]
            st.markdown(f'<div class="signal {cls}"><div class="signal-t">{sig["title"]}</div><div class="signal-m">{sig["message"]}</div></div>', unsafe_allow_html=True)
        panel_close()

    c1, c2, c3 = st.columns(3)

    with c1:
        panel_open("Sales Funnel")
        funnel = analytics.get_sales_funnel()
        fig_f = go.Figure(go.Funnel(
            y=[f["stage"] for f in funnel],
            x=[f["percentage"] for f in funnel],
            text=[f["formatted"] for f in funnel],
            textinfo="text",
            textfont=dict(color="#fff", size=11.5),
            marker=dict(color=PALETTE[:len(funnel)]),
            connector=dict(line=dict(color=BORDER, width=1))
        ))
        fig_f.update_layout(**plot_layout(height=280))
        st.plotly_chart(fig_f, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    with c2:
        panel_open("Category Revenue", "Share of total")
        cat_rev = analytics.get_category_revenue()
        fig_tm = go.Figure(go.Treemap(
            labels=[c["category"] for c in cat_rev],
            parents=[""] * len(cat_rev),
            values=[c["revenue"] for c in cat_rev],
            marker=dict(colors=PALETTE[:len(cat_rev)], line=dict(color=CARD, width=2)),
            textinfo="label+percent parent",
            textfont=dict(color="#fff", size=12),
        ))
        fig_tm.update_layout(height=280, margin=dict(l=2, r=2, t=2, b=2), paper_bgcolor=CARD)
        st.plotly_chart(fig_tm, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    with c3:
        panel_open("Sales Seasonality", "Daily density")
        seas = analytics.get_sales_seasonality()
        fig_h = go.Figure(go.Heatmap(
            z=seas["matrix"],
            colorscale=[[0, "#F3F2F1"], [0.5, "#8AD4EB"], [1, ACCENT]],
            showscale=False,
            xgap=3, ygap=3,
        ))
        fig_h.update_layout(height=280, margin=dict(l=2, r=2, t=2, b=2), paper_bgcolor=CARD,
                             xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    t_col, p_col = st.columns([2, 1])

    with t_col:
        panel_open("Recent Sales Records")
        records_data = analytics.get_sales_records(limit=8)
        rows = records_data.get("records", [])
        if rows:
            html = '<table class="rec-table"><tr><th>Order ID</th><th>Date</th><th>Customer</th><th>Amount</th><th>Status</th></tr>'
            for r in rows:
                status = str(r.get("status", "")).lower()
                pill_cls = f"pill-{status}" if f"pill-{status}" in ["pill-completed", "pill-delivered", "pill-shipped", "pill-pending", "pill-cancelled"] else "pill-default"
                raw_amount = r.get("amount", 0)
                try:
                    amount_str = f"${float(str(raw_amount).replace('$', '').replace(',', '')):,.2f}"
                except (ValueError, TypeError):
                    amount_str = str(raw_amount)
                html += f'<tr><td>{r.get("order_id","")}</td><td>{r.get("date","")}</td><td>{r.get("customer","")}</td><td>{amount_str}</td><td><span class="pill {pill_cls}">{r.get("status","")}</span></td></tr>'
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)
        panel_close()

    with p_col:
        panel_open("Daily Pattern", "Peak hours highlighted")
        pattern = analytics.get_daily_pattern()
        df_pat = pd.DataFrame(pattern)
        colors_pat = [ACCENT if r["is_peak"] else "#D2D0CE" for r in pattern]
        fig_pat = go.Figure(go.Bar(x=df_pat["hour"], y=df_pat["sales"], marker_color=colors_pat, marker_line_width=0))
        fig_pat.update_layout(**plot_layout(height=210))
        fig_pat.update_xaxes(showticklabels=False, gridcolor="rgba(0,0,0,0)")
        fig_pat.update_yaxes(showticklabels=False, gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pat, use_container_width=True, config={"displayModeBar": False})
        panel_close()


# ══════════════════════════════════════════════
#  PAGE: Product Intelligence
# ══════════════════════════════════════════════
elif page == "📦 Product":
    cat_rev = analytics.get_category_revenue()

    pc1, pc2 = st.columns(2)
    with pc1:
        panel_open("Revenue by Category")
        fig_cat = go.Figure(go.Bar(
            x=[c["category"] for c in cat_rev], y=[c["revenue"] for c in cat_rev],
            marker_color=PALETTE[:len(cat_rev)],
            text=[f'{c["percentage"]}%' for c in cat_rev], textposition="outside", textfont=dict(color="#fff")
        ))
        fig_cat.update_layout(**plot_layout(height=360))
        st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    with pc2:
        panel_open("Category Revenue Share")
        fig_pie = go.Figure(go.Pie(
            labels=[c["category"] for c in cat_rev], values=[c["revenue"] for c in cat_rev], hole=0.6,
            marker=dict(colors=PALETTE[:len(cat_rev)], line=dict(color=CARD, width=2)),
            textinfo="label+percent", textfont=dict(color="#fff")
        ))
        fig_pie.update_layout(**plot_layout(height=360))
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    prof_data = analytics.get_profitability_analysis()
    tp_col, lm_col = st.columns(2)
    with tp_col:
        panel_open("🏆 Top 5 Most Profitable Products")
        df_top = pd.DataFrame(prof_data["top_profitable"])[["Product_Name", "Revenue", "Profit", "Category"]]
        df_top.columns = ["Product", "Revenue ($)", "Profit ($)", "Category"]
        df_top["Revenue ($)"] = df_top["Revenue ($)"].apply(lambda x: f"${x:,.0f}")
        df_top["Profit ($)"] = df_top["Profit ($)"].apply(lambda x: f"${x:,.0f}")
        st.dataframe(df_top, use_container_width=True, hide_index=True)
        panel_close()

    with lm_col:
        panel_open("⚠️ Top 5 Loss-Making Products")
        df_loss = pd.DataFrame(prof_data["loss_making"])[["Product_Name", "Revenue", "Profit", "Category"]]
        df_loss.columns = ["Product", "Revenue ($)", "Profit ($)", "Category"]
        df_loss["Revenue ($)"] = df_loss["Revenue ($)"].apply(lambda x: f"${x:,.0f}")
        df_loss["Profit ($)"] = df_loss["Profit ($)"].apply(lambda x: f"${x:,.0f}")
        st.dataframe(df_loss, use_container_width=True, hide_index=True)
        panel_close()


# ══════════════════════════════════════════════
#  PAGE: Customer Intelligence (RFM)
# ══════════════════════════════════════════════
elif page == "👥 Customer":
    rfm = analytics.get_rfm_analysis()

    rc1, rc2 = st.columns([1, 1])
    with rc1:
        panel_open("RFM Customer Segmentation", f"{rfm['total_customers']:,} customers · Avg monetary ${rfm['avg_monetary']:,.0f}")
        for seg in rfm["segments"]:
            st.markdown(f"""
            <div class="rfm-row">
                <div><span class="rfm-dot" style="background:{seg['color']};"></span>
                    <span class="rfm-name">{seg['name']}</span>
                    <div class="rfm-desc">{seg['desc']}</div>
                </div>
                <span class="rfm-count" style="background:{seg['color']}22; color:{seg['color']};">{seg['count']:,}</span>
            </div>
            """, unsafe_allow_html=True)
        panel_close()

    with rc2:
        panel_open("Segment Distribution")
        fig_rfm = go.Figure(go.Pie(
            labels=[s["name"] for s in rfm["segments"]], values=[s["count"] for s in rfm["segments"]], hole=0.6,
            marker=dict(colors=[s["color"] for s in rfm["segments"]], line=dict(color=CARD, width=2)),
            textinfo="label+percent", textfont=dict(color="#fff", size=11.5),
        ))
        fig_rfm.update_layout(**plot_layout(height=380))
        st.plotly_chart(fig_rfm, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    panel_open("Segment Comparison")
    fig_seg_bar = go.Figure(go.Bar(
        x=[s["name"] for s in rfm["segments"]], y=[s["count"] for s in rfm["segments"]],
        marker_color=[s["color"] for s in rfm["segments"]],
        text=[f'{s["count"]:,}' for s in rfm["segments"]], textposition="outside", textfont=dict(color=TEXT)
    ))
    fig_seg_bar.update_layout(**plot_layout(height=300))
    st.plotly_chart(fig_seg_bar, use_container_width=True, config={"displayModeBar": False})
    panel_close()


# ══════════════════════════════════════════════
#  PAGE: Regional Intelligence
# ══════════════════════════════════════════════
elif page == "🌍 Regional":
    regional = analytics.get_regional_analysis()
    df_states = pd.DataFrame(regional["top_states"])

    rg1, rg2 = st.columns(2)
    with rg1:
        panel_open("State Revenue", "Top 10")
        fig_reg = go.Figure(go.Bar(
            x=df_states["State"], y=df_states["Revenue"], marker_color=ACCENT,
            text=df_states["Revenue"].apply(lambda v: f"${v/1e6:.1f}M"), textposition="outside", textfont=dict(color=TEXT)
        ))
        fig_reg.update_layout(**plot_layout(height=360))
        st.plotly_chart(fig_reg, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    with rg2:
        panel_open("State Profit Contribution", "Top 10")
        fig_prof = go.Figure(go.Bar(
            x=df_states["State"], y=df_states["Profit"], marker_color=ACCENT_2,
            text=df_states["Profit"].apply(lambda v: f"${v/1e6:.1f}M"), textposition="outside", textfont=dict(color=TEXT)
        ))
        fig_prof.update_layout(**plot_layout(height=360))
        st.plotly_chart(fig_prof, use_container_width=True, config={"displayModeBar": False})
        panel_close()

    panel_open("Regional Performance Table")
    display_states = df_states.copy()
    display_states["Revenue"] = display_states["Revenue"].apply(lambda x: f"${x:,.0f}")
    display_states["Profit"] = display_states["Profit"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(display_states, use_container_width=True, hide_index=True)
    panel_close()


# ══════════════════════════════════════════════
#  PAGE: Profitability & Forecast
# ══════════════════════════════════════════════
elif page == "💰 Profitability":
    pr1, pr2 = st.columns(2)

    with pr1:
        panel_open("What-If Discount Simulator")
        discount_adj = st.slider("Discount Adjustment (%)", min_value=-10, max_value=25, value=0, step=1)
        prof = analytics.get_profitability_analysis(discount_adjustment=discount_adj)

        w1, w2, w3 = st.columns(3)
        w1.markdown(f'<div class="wif"><span>Projected Revenue</span><h4>${prof["what_if"]["adjusted_revenue"]:,.0f}</h4></div>', unsafe_allow_html=True)
        w2.markdown(f'<div class="wif"><span>Projected Profit</span><h4>${prof["what_if"]["adjusted_profit"]:,.0f}</h4></div>', unsafe_allow_html=True)
        w3.markdown(f'<div class="wif"><span>Projected Margin</span><h4>{prof["what_if"]["adjusted_margin"]:.1f}%</h4></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Baseline Revenue", f"${prof['baseline']['revenue']:,.0f}")
        b2.metric("Baseline Cost", f"${prof['baseline']['cost']:,.0f}")
        b3.metric("Baseline Profit", f"${prof['baseline']['profit']:,.0f}")
        b4.metric("Baseline Margin", f"{prof['baseline']['margin']:.1f}%")
        panel_close()

    with pr2:
        panel_open("6-Month Revenue Forecast")
        forecast = analytics.get_forecast()
        all_labels = forecast["historical_labels"] + forecast["forecast_labels"]
        hist_vals = forecast["historical_values"] + [None] * len(forecast["forecast_labels"])
        fore_vals = [None] * (len(forecast["historical_values"]) - 1) + [forecast["historical_values"][-1]] + forecast["forecast_values"]

        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(x=all_labels, y=hist_vals, mode="lines", name="Historical", line=dict(color=ACCENT, width=2.5)))
        fig_fc.add_trace(go.Scatter(x=all_labels, y=fore_vals, mode="lines", name="Forecast", line=dict(color=ACCENT_2, width=2.5, dash="dot")))
        fig_fc.update_layout(**plot_layout(height=340, showlegend=True))
        st.plotly_chart(fig_fc, use_container_width=True, config={"displayModeBar": False})
        panel_close()


# ══════════════════════════════════════════════
#  PAGE: AI Analytics Assistant
# ══════════════════════════════════════════════
elif page == "🤖 AI Assistant":
    st.caption("Ask natural language questions about your e-commerce data")

    if "ai_history" not in st.session_state:
        st.session_state.ai_history = [
            {"role": "ai", "text": 'Hello! I am your **ShopPulse AI Analytics Assistant**. Ask me anything about sales, revenue, products, customers, or margins. Try *"What is total revenue?"* or *"Show customer segments"*.'}
        ]

    panel_open("Conversation")
    for msg in st.session_state.ai_history:
        cls = "chat-ai" if msg["role"] == "ai" else "chat-user"
        st.markdown(f'<div class="{cls}">{msg["text"]}</div>', unsafe_allow_html=True)
    panel_close()

    query = st.chat_input("Ask a business query (e.g. Total profit margin, top customers)...")
    if query:
        st.session_state.ai_history.append({"role": "user", "text": query})
        answer = analytics.answer_ai_query(query)
        st.session_state.ai_history.append({"role": "ai", "text": answer})
        st.rerun()