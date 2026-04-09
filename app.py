import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
# Resolve data directory (works wherever you run from)
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy – Route Efficiency",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0f1117; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d2e 0%, #0f1117 100%);
        border-right: 1px solid #2d2f45;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e2130 0%, #252840 100%);
        border: 1px solid #3a3d5c;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        border-color: #7c83fd;
        box-shadow: 0 4px 15px rgba(124,131,253,0.15);
    }
    
    .metric-card .label {
        font-size: 12px;
        color: #8b8fa8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .metric-card .value {
        font-size: 28px;
        font-weight: 700;
        color: #e8eaf6;
    }
    .metric-card .delta {
        font-size: 12px;
        color: #7c83fd;
        margin-top: 4px;
        font-weight: 500;
    }
    
    .section-header {
        background: linear-gradient(90deg, #7c83fd22, transparent);
        border-left: 3px solid #7c83fd;
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        margin: 20px 0 16px 0;
        font-size: 16px;
        font-weight: 600;
        color: #c5cae9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1d2e;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8b8fa8;
        font-weight: 500;
        border-radius: 8px;
        padding: 8px 20px;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c83fd, #a78bfa) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(124,131,253,0.2);
    }
    
    div[data-testid="stDataFrame"] { 
        border-radius: 10px; 
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .sidebar-title {
        font-size: 20px;
        font-weight: 700;
        color: #e8eaf6;
        padding: 8px 0 16px 0;
        border-bottom: 1px solid #2d2f45;
        margin-bottom: 20px;
    }

    .logo-text {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg, #7c83fd, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .bottleneck-badge {
        display: inline-block;
        background: #ff6b6b22;
        border: 1px solid #ff6b6b66;
        color: #ff9999;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }
    .good-badge {
        display: inline-block;
        background: #51cf6622;
        border: 1px solid #51cf6666;
        color: #69db7c;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .filter-info {
        background: linear-gradient(135deg, #1e2130 0%, #252840 100%);
        border: 1px solid #3a3d5c;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        font-size: 12px;
        color: #a78bfa;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Factory coordinates (from PRD)
# ─────────────────────────────────────────────
FACTORY_COORDS = {
    "Lot's O' Nuts":    {"lat": 32.881893, "lon": -111.768036, "state": "AZ"},
    "Wicked Choccy's":  {"lat": 32.076176, "lon": -81.088371,  "state": "GA"},
    "Sugar Shack":      {"lat": 48.11914,  "lon": -96.18115,   "state": "MN"},
    "Secret Factory":   {"lat": 41.446333, "lon": -90.565487,  "state": "IL"},
    "The Other Factory":{"lat": 35.1175,   "lon": -89.971107,  "state": "TN"},
}

# US state abbreviation map (for choropleth)
STATE_ABBREV = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY', 'District Of Columbia': 'DC',
    'Alberta': 'AB', 'British Columbia': 'BC', 'Manitoba': 'MB',
    'Ontario': 'ON', 'Quebec': 'QC', 'Saskatchewan': 'SK',
    'Prince Edward Island': 'PE', 'New Brunswick': 'NB', 'Nova Scotia': 'NS',
}

# ─────────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, "nassau_final.csv"))
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"])
    df["State_Abbrev"] = df["State/Province"].map(STATE_ABBREV)
    df["Route_State"] = df["Factory"] + " → " + df["State/Province"]
    df["Route_Region"] = df["Factory"] + " → " + df["Region"]
    df["Shipping Category"] = df["Ship Mode"].apply(
        lambda x: "Expedited" if x in ["First Class", "Second Class", "Same Day"] else "Standard"
    )
    return df

@st.cache_data
def load_route_region():
    return pd.read_csv(os.path.join(BASE_DIR, "nassau_route_region.csv"))

@st.cache_data
def load_route_states():
    return pd.read_csv(os.path.join(BASE_DIR, "nassau_route_states.csv"))

@st.cache_data
def load_ship_mode():
    return pd.read_csv(os.path.join(BASE_DIR, "ship_mode_group.csv"))

df_full   = load_data()
rr        = load_route_region()
rs        = load_route_states()
sm        = load_ship_mode()

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c5cae9", family="Inter"),
    xaxis=dict(gridcolor="#2d2f45", linecolor="#3a3d5c", tickcolor="#8b8fa8"),
    yaxis=dict(gridcolor="#2d2f45", linecolor="#3a3d5c", tickcolor="#8b8fa8"),
    legend=dict(bgcolor="rgba(30,33,48,0.8)", bordercolor="#3a3d5c", borderwidth=1),
    margin=dict(l=20, r=20, t=40, b=20),
)
COLORS = ["#7c83fd","#a78bfa","#f472b6","#fb923c","#34d399","#60a5fa","#fbbf24","#e879f9"]

# ─────────────────────────────────────────────
# SIDEBAR – ENHANCED with MULTISELECT
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🍬 Nassau Candy</div>', unsafe_allow_html=True)
    st.markdown("**Shipping Route Intelligence**")
    st.markdown("---")

    st.markdown("### 🎛️ Advanced Filters")

    # Date Range Filter
    date_min = df_full["Order Date"].min().date()
    date_max = df_full["Order Date"].max().date()
    date_range = st.date_input(
        "📅 Order Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

    # Region Filter – MULTISELECT
    all_regions = sorted(df_full["Region"].dropna().unique().tolist())
    sel_regions = st.multiselect(
        "🗺️ Region",
        options=all_regions,
        default=all_regions,
        help="Select one or more regions to analyze"
    )
    
    if len(sel_regions) > 0:
        st.markdown(f'<div class="filter-info">✅ {len(sel_regions)} region(s) selected</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please select at least one region")

    # State Filter
    if sel_regions:
        available_states = sorted(df_full[df_full["Region"].isin(sel_regions)]["State/Province"].dropna().unique().tolist())
    else:
        available_states = sorted(df_full["State/Province"].dropna().unique().tolist())
    
    sel_state = st.selectbox("📍 State / Province", ["All States"] + available_states)

    # Ship Mode Filter – MULTISELECT
    all_ship_modes = sorted(df_full["Ship Mode"].dropna().unique().tolist())
    sel_ship_modes = st.multiselect(
        "🚚 Ship Mode",
        options=all_ship_modes,
        default=all_ship_modes,
        help="Select one or more shipping modes"
    )
    
    if len(sel_ship_modes) > 0:
        st.markdown(f'<div class="filter-info">✅ {len(sel_ship_modes)} ship mode(s) selected</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please select at least one ship mode")

    # Lead Time Threshold
    avg_lt = int(df_full["Lead Time"].mean())
    lt_threshold = st.slider(
        "⏱️ Lead-Time Threshold (days)",
        min_value=int(df_full["Lead Time"].min()),
        max_value=int(df_full["Lead Time"].max()),
        value=avg_lt,
        step=10,
    )

    st.markdown("---")
    st.caption("Nassau Candy Distributor · Route Efficiency Intelligence Platform")
    
    
    st.sidebar.markdown("### 📌 Project Info")

    st.sidebar.caption("Organization")
    st.sidebar.markdown("[Unified Mentor](https://unifiedmentor.com/)")
    st.sidebar.caption("Instructor")
    st.sidebar.markdown("[Saiprasad Kagne](https://saikagne.github.io/)")
    st.sidebar.caption("Analyst")
    st.sidebar.markdown("[Shreyash Ambade](https://www.linkedin.com/in/shreyash-ambade-193a2220a/)")
    
# ─────────────────────────────────────────────
# Apply Filters
# ─────────────────────────────────────────────
dff = df_full.copy()

if len(date_range) == 2:
    dff = dff[
        (dff["Order Date"] >= pd.Timestamp(date_range[0])) &
        (dff["Order Date"] <= pd.Timestamp(date_range[1]))
    ]

# Apply Region filter (multiselect)
if len(sel_regions) > 0:
    dff = dff[dff["Region"].isin(sel_regions)]

# Apply State filter
if sel_state != "All States":
    dff = dff[dff["State/Province"] == sel_state]

# Apply Ship Mode filter (multiselect)
if len(sel_ship_modes) > 0:
    dff = dff[dff["Ship Mode"].isin(sel_ship_modes)]

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

st.title('🍬 Nassau Candy Distributor')
st.markdown('<span class="logo-text">Nassau Candy — Route Efficiency Dashboard</span>', unsafe_allow_html=True)
st.caption("🔍 Factory-to-Customer Shipping Intelligence Platform")

st.markdown("---")

# ─────────────────────────────────────────────
# KPI Row
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
total_orders = len(dff)
avg_lead     = dff["Lead Time"].mean() if total_orders else 0
delayed_pct  = (dff["Lead Time"] > lt_threshold).mean() * 100 if total_orders else 0
total_sales  = dff["Sales"].sum()
total_profit = dff["Gross Profit"].sum()

metrics = [
    (k1, "Total Shipments",   f"{total_orders:,}",          "from filtered range"),
    (k2, "Avg Lead Time",     f"{avg_lead:.0f} days",       "mean across routes"),
    (k3, "Delay Rate",        f"{delayed_pct:.1f}%",        f"above {lt_threshold}d threshold"),
    (k4, "Total Sales",       f"${total_sales:,.0f}",       "gross revenue"),
    (k5, "Total Gross Profit",f"${total_profit:,.0f}",      "sum of profits"),
]
for col, label, value, delta in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="delta">{delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Route Efficiency Overview",
    "🗺️ Geographic Map",
    "🚚 Ship Mode Comparison",
    "🔍 Route Drill-Down",
])

# ══════════════════════════════════════════════
# TAB 1 – ROUTE EFFICIENCY OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Average Lead Time by Route (Region Level)</div>', unsafe_allow_html=True)

    # Build region-route summary from filtered data
    rr_filtered = dff.groupby("Route_Region").agg(
        Total_Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
    ).reset_index().rename(columns={"Route_Region": "Route"})
    rr_filtered["Avg_Lead_Time"] = rr_filtered["Avg_Lead_Time"].round(1)
    rr_filtered = rr_filtered.sort_values("Avg_Lead_Time")

    if len(rr_filtered) == 0:
        st.info("No data available for selected filters.")
    else:
        fig_bar = px.bar(
            rr_filtered, x="Avg_Lead_Time", y="Route",
            orientation="h",
            color="Avg_Lead_Time",
            color_continuous_scale=["#34d399", "#7c83fd", "#f472b6", "#ef4444"],
            text="Avg_Lead_Time",
            hover_data={"Total_Shipments": True, "Total_Sales": ":.2f", "Total_Profit": ":.2f"},
            labels={"Avg_Lead_Time": "Avg Lead Time (days)", "Route": ""},
        )
        fig_bar.update_traces(texttemplate="%{text:.0f}d", textposition="outside")
        fig_bar.update_coloraxes(showscale=False)
        fig_bar.update_layout(**PLOTLY_THEME, height=520, title="Average Lead Time by Factory→Region Route")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<div class="section-header">Route Performance Leaderboard (State Level)</div>', unsafe_allow_html=True)

    rs_filtered = dff.groupby("Route_State").agg(
        Total_Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Lead_Time_Std=("Lead Time", "std"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Delay_Rate=("Is Delay", "mean"),
    ).reset_index()
    rs_filtered["Avg_Lead_Time"]  = rs_filtered["Avg_Lead_Time"].round(1)
    rs_filtered["Lead_Time_Std"]  = rs_filtered["Lead_Time_Std"].fillna(0).round(1)
    rs_filtered["Delay_Rate"]     = (rs_filtered["Delay_Rate"] * 100).round(1)

    if len(rs_filtered) > 0:
        min_lt = rs_filtered["Avg_Lead_Time"].min()
        max_lt = rs_filtered["Avg_Lead_Time"].max()
        rs_filtered["Efficiency_Score"] = (
            1 - (rs_filtered["Avg_Lead_Time"] - min_lt) / (max_lt - min_lt + 1e-9)
        ).round(3)

        rs_filtered = rs_filtered.sort_values("Avg_Lead_Time")
        rs_filtered["Rank"] = range(1, len(rs_filtered) + 1)

        c_top, c_bot = st.columns(2)
        with c_top:
            st.markdown("#### 🏆 Top 10 Most Efficient Routes")
            top10 = rs_filtered.head(10)[["Rank","Route_State","Avg_Lead_Time","Lead_Time_Std","Efficiency_Score","Delay_Rate"]]
            top10.columns = ["Rank","Route","Avg Days","Variability","Eff. Score","Delay %"]
            st.dataframe(top10.set_index("Rank"), use_container_width=True, height=340)

        with c_bot:
            st.markdown("#### 🐢 Bottom 10 Least Efficient Routes")
            bot10 = rs_filtered.tail(10).sort_values("Avg_Lead_Time", ascending=False)[
                ["Rank","Route_State","Avg_Lead_Time","Lead_Time_Std","Efficiency_Score","Delay_Rate"]
            ]
            bot10.columns = ["Rank","Route","Avg Days","Variability","Eff. Score","Delay %"]
            st.dataframe(bot10.set_index("Rank"), use_container_width=True, height=340)

        # Efficiency score scatter
        st.markdown('<div class="section-header">Efficiency Score vs. Volume (Bubble Chart)</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            rs_filtered,
            x="Avg_Lead_Time", y="Efficiency_Score",
            size="Total_Shipments", color="Delay_Rate",
            hover_name="Route_State",
            color_continuous_scale="RdYlGn_r",
            labels={
                "Avg_Lead_Time": "Avg Lead Time (days)",
                "Efficiency_Score": "Efficiency Score (1=best)",
                "Delay_Rate": "Delay %",
            },
            size_max=40,
        )
        fig_scatter.update_layout(**PLOTLY_THEME, height=420, title="Route Efficiency Score vs Avg Lead Time")
        fig_scatter.update_coloraxes(colorbar_title="Delay %")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No route data available for selected filters.")


# ══════════════════════════════════════════════
# TAB 2 – GEOGRAPHIC MAP
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">US Heatmap – Shipping Efficiency by State</div>', unsafe_allow_html=True)

    state_summary = dff.groupby("State/Province").agg(
        Total_Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Delay_Rate=("Is Delay", "mean"),
        Total_Sales=("Sales", "sum"),
    ).reset_index()
    state_summary["Avg_Lead_Time"] = state_summary["Avg_Lead_Time"].round(1)
    state_summary["Delay_Rate"]    = (state_summary["Delay_Rate"] * 100).round(1)
    state_summary["State_Abbrev"]  = state_summary["State/Province"].map(STATE_ABBREV)

    if len(state_summary) == 0:
        st.info("No state data available for selected filters.")
    else:
        map_metric = st.radio(
            "Colour by:", ["Avg Lead Time", "Delay Rate %", "Total Shipments"],
            horizontal=True,
        )
        col_map = {"Avg Lead Time": "Avg_Lead_Time", "Delay Rate %": "Delay_Rate", "Total Shipments": "Total_Shipments"}
        scale_map = {"Avg Lead Time": "RdYlGn_r", "Delay Rate %": "Reds", "Total Shipments": "Blues"}

        fig_choro = px.choropleth(
            state_summary.dropna(subset=["State_Abbrev"]),
            locations="State_Abbrev",
            locationmode="USA-states",
            color=col_map[map_metric],
            color_continuous_scale=scale_map[map_metric],
            scope="usa",
            hover_name="State/Province",
            hover_data={
                "Avg_Lead_Time": True,
                "Delay_Rate": True,
                "Total_Shipments": True,
                "State_Abbrev": False,
            },
            labels={"Avg_Lead_Time": "Avg Days", "Delay_Rate": "Delay %", "Total_Shipments": "Shipments"},
        )
        fig_choro.update_layout(
            geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)", landcolor="#1e2130",
                     subunitcolor="#3a3d5c"),
            **PLOTLY_THEME, height=480,
            title=f"US State-Level Shipping – {map_metric}",
        )
        st.plotly_chart(fig_choro, use_container_width=True)

        # Factory markers overlay description
        st.markdown('<div class="section-header">Factory Locations & Bottleneck Regions</div>', unsafe_allow_html=True)

        avg_all_lt = dff["Lead Time"].mean()
        avg_all_sh = dff.groupby("State/Province").size().mean()

        bottlenecks = state_summary[
            (state_summary["Avg_Lead_Time"] > avg_all_lt) &
            (state_summary["Total_Shipments"] > avg_all_sh)
        ].sort_values("Avg_Lead_Time", ascending=False)

        c_map1, c_map2 = st.columns([2, 1])
        with c_map1:
            factory_df = pd.DataFrame([
                {"Name": k, "Lat": v["lat"], "Lon": v["lon"], "Type": "Factory"}
                for k, v in FACTORY_COORDS.items()
            ])

            fig_map2 = go.Figure()
            fig_map2.add_trace(go.Scattergeo(
                lat=factory_df["Lat"], lon=factory_df["Lon"],
                text=factory_df["Name"],
                mode="markers+text",
                marker=dict(size=14, color="#fbbf24", symbol="star", line=dict(width=1, color="#fff")),
                textposition="top center",
                textfont=dict(color="#fbbf24", size=10),
                name="Factories",
            ))
            fig_map2.update_layout(
                geo=dict(scope="usa", bgcolor="rgba(0,0,0,0)", landcolor="#1e2130",
                         subunitcolor="#3a3d5c", lakecolor="rgba(0,0,0,0)"),
                **PLOTLY_THEME, height=380, title="Factory Locations (USA)",
            )
            st.plotly_chart(fig_map2, use_container_width=True)

        with c_map2:
            st.markdown("#### 🔴 Bottleneck States")
            st.caption("High volume + above-avg lead time")
            if len(bottlenecks) == 0:
                st.info("No bottlenecks with current filters.")
            else:
                for _, row in bottlenecks.head(12).iterrows():
                    badge = "🔴" if row["Avg_Lead_Time"] > avg_all_lt * 1.05 else "🟡"
                    st.markdown(
                        f"{badge} **{row['State/Province']}** &nbsp; "
                        f"`{row['Avg_Lead_Time']:.0f}d` &nbsp; {row['Total_Shipments']} shipments"
                    )

        # Region bottleneck bar
        st.markdown('<div class="section-header">Regional Bottleneck Comparison</div>', unsafe_allow_html=True)
        region_sum = dff.groupby("Region").agg(
            Total_Shipments=("Order ID","count"),
            Avg_Lead_Time=("Lead Time","mean"),
            Delay_Rate=("Is Delay","mean"),
        ).reset_index()
        region_sum["Delay_Rate"] = (region_sum["Delay_Rate"]*100).round(1)
        region_sum["Avg_Lead_Time"] = region_sum["Avg_Lead_Time"].round(1)

        if len(region_sum) > 0:
            fig_reg = make_subplots(specs=[[{"secondary_y": True}]])
            fig_reg.add_trace(go.Bar(
                x=region_sum["Region"], y=region_sum["Avg_Lead_Time"],
                name="Avg Lead Time (days)", marker_color=COLORS[0],
            ), secondary_y=False)
            fig_reg.add_trace(go.Scatter(
                x=region_sum["Region"], y=region_sum["Delay_Rate"],
                name="Delay Rate %", mode="lines+markers",
                marker=dict(color=COLORS[2], size=8), line=dict(color=COLORS[2], width=2),
            ), secondary_y=True)
            fig_reg.update_layout(**PLOTLY_THEME, height=360, title="Region: Avg Lead Time & Delay Rate")
            fig_reg.update_yaxes(title_text="Avg Lead Time (days)", secondary_y=False, gridcolor="#2d2f45")
            fig_reg.update_yaxes(title_text="Delay Rate %", secondary_y=True, gridcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_reg, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 – SHIP MODE COMPARISON
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Lead Time Comparison by Shipping Method</div>', unsafe_allow_html=True)

    sm_filtered = dff.groupby("Ship Mode").agg(
        Total_Shipments=("Order ID","count"),
        Avg_Lead_Time=("Lead Time","mean"),
        Lead_Time_Std=("Lead Time","std"),
        Total_Sales=("Sales","sum"),
        Avg_Cost=("Cost","mean"),
        Avg_Profit=("Gross Profit","mean"),
        Delay_Rate=("Is Delay","mean"),
    ).reset_index()
    sm_filtered["Avg_Lead_Time"] = sm_filtered["Avg_Lead_Time"].round(2)
    sm_filtered["Lead_Time_Std"] = sm_filtered["Lead_Time_Std"].round(2)
    sm_filtered["Delay_Rate"]    = (sm_filtered["Delay_Rate"]*100).round(1)
    sm_filtered["Avg_Cost"]      = sm_filtered["Avg_Cost"].round(2)
    sm_filtered["Avg_Profit"]    = sm_filtered["Avg_Profit"].round(2)
    sm_filtered = sm_filtered.sort_values("Avg_Lead_Time")

    if len(sm_filtered) == 0:
        st.info("No ship mode data available for selected filters.")
    else:
        c_s1, c_s2, c_s3, c_s4 = st.columns(4)
        for i, (col, row) in enumerate(zip([c_s1,c_s2,c_s3,c_s4], sm_filtered.itertuples())):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="label">{row._1}</div>
                    <div class="value">{row.Avg_Lead_Time:.0f}d</div>
                    <div class="delta">{row.Total_Shipments:,} shipments · {row.Delay_Rate}% delayed</div>
                </div>""", unsafe_allow_html=True)

        c_sh1, c_sh2 = st.columns(2)

        with c_sh1:
            # Lead time distribution violin
            fig_viol = px.violin(
                dff, x="Ship Mode", y="Lead Time",
                color="Ship Mode", color_discrete_sequence=COLORS,
                box=True, points=False,
                labels={"Lead Time": "Lead Time (days)", "Ship Mode": ""},
            )
            fig_viol.update_layout(**PLOTLY_THEME, height=380, title="Lead Time Distribution by Ship Mode",
                                   showlegend=False)
            st.plotly_chart(fig_viol, use_container_width=True)

        with c_sh2:
            # Delay rate bar
            fig_delay = px.bar(
                sm_filtered, x="Ship Mode", y="Delay_Rate",
                color="Ship Mode", color_discrete_sequence=COLORS,
                text="Delay_Rate",
                labels={"Delay_Rate": "Delay Rate %", "Ship Mode": ""},
            )
            fig_delay.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_delay.update_layout(**PLOTLY_THEME, height=380, title="Delay Rate % by Ship Mode",
                                    showlegend=False)
            st.plotly_chart(fig_delay, use_container_width=True)

        st.markdown('<div class="section-header">Standard vs Expedited – Cost-Time Trade-off</div>', unsafe_allow_html=True)

        cat_df = dff.groupby("Shipping Category").agg(
            Total_Shipments=("Order ID","count"),
            Avg_Lead_Time=("Lead Time","mean"),
            Lead_Time_Std=("Lead Time","std"),
            Total_Sales=("Sales","sum"),
            Avg_Cost=("Cost","mean"),
            Avg_Profit=("Gross Profit","mean"),
            Delay_Rate=("Is Delay","mean"),
        ).reset_index()
        cat_df["Delay_Rate"]    = (cat_df["Delay_Rate"]*100).round(2)
        cat_df["Avg_Lead_Time"] = cat_df["Avg_Lead_Time"].round(2)
        cat_df["Avg_Sales_Per_Shipment"] = (cat_df["Total_Sales"]/cat_df["Total_Shipments"]).round(2)

        if len(cat_df) > 0:
            c_c1, c_c2 = st.columns(2)
            with c_c1:
                comp_data = []
                for _, row in cat_df.iterrows():
                    comp_data.append({"Category": row["Shipping Category"], "Metric": "Avg Cost ($)", "Value": row["Avg_Cost"]})
                    comp_data.append({"Category": row["Shipping Category"], "Metric": "Avg Profit ($)", "Value": row["Avg_Profit"]})
                    comp_data.append({"Category": row["Shipping Category"], "Metric": "Avg Sales/Shipment", "Value": row["Avg_Sales_Per_Shipment"]})

                comp_df = pd.DataFrame(comp_data)
                fig_comp = px.bar(comp_df, x="Metric", y="Value", color="Category",
                                  barmode="group", color_discrete_sequence=COLORS,
                                  text_auto=".2f")
                fig_comp.update_layout(**PLOTLY_THEME, height=360, title="Cost & Profit: Standard vs Expedited")
                st.plotly_chart(fig_comp, use_container_width=True)

            with c_c2:
                # Scatter: avg lead time vs avg profit per category
                fig_tradeoff = px.scatter(
                    cat_df, x="Avg_Lead_Time", y="Avg_Profit",
                    size="Total_Shipments", color="Shipping Category",
                    color_discrete_sequence=COLORS,
                    text="Shipping Category",
                    labels={"Avg_Lead_Time": "Avg Lead Time (days)", "Avg_Profit": "Avg Gross Profit ($)"},
                    size_max=50,
                )
                fig_tradeoff.update_traces(textposition="top center")
                fig_tradeoff.update_layout(**PLOTLY_THEME, height=360, title="Cost-Time Trade-off")
                st.plotly_chart(fig_tradeoff, use_container_width=True)

        # Summary table
        st.markdown("#### 📋 Ship Mode Full Summary")
        display_sm = sm_filtered.copy()
        display_sm.columns = ["Ship Mode","Total Shipments","Avg Lead Time","Variability","Total Sales","Avg Cost","Avg Profit","Delay Rate %"]
        st.dataframe(display_sm.set_index("Ship Mode"), use_container_width=True)


# ══════════════════════════════════════════════
# TAB 4 – ROUTE DRILL-DOWN
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">State-Level Route Performance Insights</div>', unsafe_allow_html=True)

    c_d1, c_d2 = st.columns([1, 2])
    with c_d1:
        all_routes = sorted(dff["Route_State"].dropna().unique().tolist())
        if len(all_routes) == 0:
            st.warning("No routes available for selected filters.")
        else:
            sel_route = st.selectbox("Select a Route (Factory→State)", all_routes)

            route_df = dff[dff["Route_State"] == sel_route].copy()
            route_df["Order Date"] = pd.to_datetime(route_df["Order Date"])

            with c_d2:
                if len(route_df):
                    r_avg  = route_df["Lead Time"].mean()
                    r_max  = route_df["Lead Time"].max()
                    r_min  = route_df["Lead Time"].min()
                    r_del  = (route_df["Lead Time"] > lt_threshold).mean() * 100
                    r_sal  = route_df["Sales"].sum()
                    r_pro  = route_df["Gross Profit"].sum()
                    cols   = st.columns(6)
                    for col, lbl, val in zip(cols,
                        ["Shipments","Avg Days","Min Days","Max Days","Delay %","Revenue"],
                        [f"{len(route_df):,}", f"{r_avg:.0f}", f"{r_min}", f"{r_max}", f"{r_del:.1f}%", f"${r_sal:,.0f}"]
                    ):
                        col.metric(lbl, val)

            if len(route_df) == 0:
                st.warning("No data for this route with current filters.")
            else:
                c_r1, c_r2 = st.columns(2)

                with c_r1:
                    # Lead time histogram for this route
                    fig_hist = px.histogram(
                        route_df, x="Lead Time", nbins=30,
                        color_discrete_sequence=[COLORS[0]],
                        labels={"Lead Time": "Lead Time (days)"},
                    )
                    fig_hist.add_vline(x=r_avg, line_dash="dash", line_color=COLORS[2],
                                       annotation_text=f"Mean {r_avg:.0f}d", annotation_font_color=COLORS[2])
                    fig_hist.add_vline(x=lt_threshold, line_dash="dot", line_color=COLORS[3],
                                       annotation_text=f"Threshold {lt_threshold}d", annotation_font_color=COLORS[3])
                    fig_hist.update_layout(**PLOTLY_THEME, height=340,
                                           title=f"Lead Time Distribution – {sel_route}")
                    st.plotly_chart(fig_hist, use_container_width=True)

                with c_r2:
                    # Ship mode breakdown for this route
                    sm_route = route_df.groupby("Ship Mode").agg(
                        Count=("Order ID","count"),
                        Avg_LT=("Lead Time","mean"),
                    ).reset_index()
                    fig_sm_route = px.bar(
                        sm_route, x="Ship Mode", y="Avg_LT",
                        color="Ship Mode", color_discrete_sequence=COLORS,
                        text="Count",
                        labels={"Avg_LT": "Avg Lead Time (days)"},
                    )
                    fig_sm_route.update_traces(texttemplate="%{text} orders", textposition="outside")
                    fig_sm_route.update_layout(**PLOTLY_THEME, height=340,
                                               title="Avg Lead Time by Ship Mode on this Route",
                                               showlegend=False)
                    st.plotly_chart(fig_sm_route, use_container_width=True)

                # Order-level shipment timeline
                st.markdown('<div class="section-header">Order-Level Shipment Timeline</div>', unsafe_allow_html=True)

                timeline_df = route_df.sort_values("Order Date")[
                    ["Order Date","Ship Date","Lead Time","Ship Mode","Product Name","Sales","Is Delay"]
                ].copy()
                timeline_df["Order Date"] = timeline_df["Order Date"].dt.strftime("%Y-%m-%d")
                timeline_df["Ship Date"]  = pd.to_datetime(timeline_df["Ship Date"]).dt.strftime("%Y-%m-%d")
                timeline_df["Status"]     = timeline_df["Is Delay"].map({True: "⚠️ Delayed", False: "✅ On Time"})

                # Lead time over time scatter
                route_df2 = route_df.copy()
                route_df2["Order_Month"] = route_df2["Order Date"].dt.to_period("M").astype(str)

                fig_timeline = px.scatter(
                    route_df2.head(500), x="Order Date", y="Lead Time",
                    color="Ship Mode", color_discrete_sequence=COLORS,
                    opacity=0.6, size_max=6,
                    hover_data={"Product Name": True, "Sales": True, "Is Delay": True},
                    labels={"Lead Time": "Lead Time (days)"},
                )
                fig_timeline.add_hline(y=lt_threshold, line_dash="dot", line_color=COLORS[3],
                                       annotation_text=f"Threshold ({lt_threshold}d)", annotation_font_color=COLORS[3])
                fig_timeline.update_layout(**PLOTLY_THEME, height=380,
                                           title=f"Shipment Lead Times Over Time – {sel_route} (first 500 shown)")
                st.plotly_chart(fig_timeline, use_container_width=True)

                # Raw order table
                st.markdown("#### ���� Order-Level Records (last 200)")
                display_tl = timeline_df.tail(200)[
                    ["Order Date","Ship Date","Lead Time","Ship Mode","Product Name","Sales","Status"]
                ].reset_index(drop=True)
                st.dataframe(display_tl, use_container_width=True, height=340)

                # Factory comparison across all states
                st.markdown('<div class="section-header">Factory-Level Performance Summary</div>', unsafe_allow_html=True)
                factory_sum = dff.groupby("Factory").agg(
                    Total_Shipments=("Order ID","count"),
                    Avg_Lead_Time=("Lead Time","mean"),
                    Delay_Rate=("Is Delay","mean"),
                    Total_Revenue=("Sales","sum"),
                    Total_Profit=("Gross Profit","sum"),
                    Unique_States=("State/Province","nunique"),
                ).reset_index()
                factory_sum["Avg_Lead_Time"] = factory_sum["Avg_Lead_Time"].round(1)
                factory_sum["Delay_Rate"]    = (factory_sum["Delay_Rate"]*100).round(1)

                if len(factory_sum) > 0:
                    fig_factory = px.bar(
                        factory_sum.sort_values("Avg_Lead_Time"),
                        x="Factory", y="Avg_Lead_Time",
                        color="Delay_Rate",
                        color_continuous_scale="RdYlGn_r",
                        text="Total_Shipments",
                        hover_data={"Total_Revenue": ":.2f", "Unique_States": True},
                        labels={"Avg_Lead_Time": "Avg Lead Time (days)", "Delay_Rate": "Delay %"},
                    )
                    fig_factory.update_traces(texttemplate="%{text:,} ships", textposition="outside")
                    fig_factory.update_layout(**PLOTLY_THEME, height=380, title="Factory Performance – Avg Lead Time & Delay Rate")
                    fig_factory.update_coloraxes(colorbar_title="Delay %")
                    st.plotly_chart(fig_factory, use_container_width=True)
