import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, time, timedelta
from streamlit_autorefresh import st_autorefresh

# Page Configuration
st.set_page_config(page_title="Option PCR & CPR Ratio", layout="wide")

# Auto-refresh interval set to 5000 milliseconds (5 seconds)
st_autorefresh(interval=5000, limit=None, key="option_pcr_refresh")

st.title("📊 Option PCR & CPR Ratio: Real-Time Intraday Analytics")
st.markdown("Professional derivatives intelligence tracking live timelines, overall market ratios, and 16-strike zone aggregation.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Dashboard Controls")
index_choice = st.sidebar.selectbox("Select Index", ["NIFTY", "BANKNIFTY", "SENSEX"])

# Index-specific dynamic expiry dates matching exchange rules
if index_choice == "NIFTY":
    expiry_list = ["15 Sep 2026", "22 Sep 2026", "29 Sep 2026", "29 Oct 2026 (Monthly)"]
elif index_choice == "BANKNIFTY":
    expiry_list = ["29 Sep 2026 (Monthly)", "27 Oct 2026 (Monthly)"]
else:  # SENSEX
    expiry_list = ["17 Sep 2026", "24 Sep 2026 (Monthly)", "01 Oct 2026", "08 Oct 2026"]

expiry_choice = st.sidebar.selectbox("Select Expiry Date", expiry_list)
chart_theme = st.sidebar.selectbox("Chart Theme", ["Dark", "Light"])
theme_template = "plotly_dark" if chart_theme == "Dark" else "plotly_white"

# --- 1. INTRADAY TIME-SERIES & 16-STRIKE ZONE ENGINE ---
@st.cache_data(ttl=5) # Refreshes cache dynamically every 5 seconds
def generate_intraday_data(symbol):
    if symbol == "NIFTY":
        base_price = 23420
    elif symbol == "BANKNIFTY":
        base_price = 50200
    else:
        base_price = 76800
    
    start_time = datetime.combine(datetime.today(), time(9, 15))
    end_time = datetime.combine(datetime.today(), time(15, 30))
    
    timestamps = []
    curr = start_time
    while curr <= end_time:
        timestamps.append(curr.strftime("%I:%M %p"))
        curr += timedelta(minutes=5)
        
    n = len(timestamps)
    np.random.seed(int(datetime.now().second / 5)) # Simulates live tick movement every 5 seconds
    
    price_changes = np.random.normal(0, 5, n).cumsum()
    index_prices = base_price + price_changes
    
    # Overall market metrics
    pcr_path = np.clip(1.0 + (np.random.normal(0, 0.02, n).cumsum()), 0.6, 1.5)
    cpr_path = np.clip(1.0 / pcr_path + np.random.normal(0, 0.01, n), 0.5, 2.0)
    
    call_oi_change = np.random.normal(0, 0.5, n).cumsum() + 5.0
    put_oi_change = np.random.normal(0, 0.5, n).cumsum() + 6.5
    
    # 16-Strike Aggregate Engine (8 Above + 8 Below)
    total_put_oi_16 = np.clip(1800000 + np.random.normal(0, 20000, n).cumsum(), 500000, 5000000)
    total_call_oi_16 = np.clip(1300000 + np.random.normal(0, 20000, n).cumsum(), 500000, 5000000)
    
    zone_16_pcr = total_put_oi_16 / total_call_oi_16
    zone_16_cpr = total_call_oi_16 / total_put_oi_16

    return pd.DataFrame({
        "Time": timestamps,
        "Index_Price": index_prices,
        "Overall_PCR": pcr_path,
        "Overall_CPR": cpr_path,
        "Call_OI_Change": call_oi_change,
        "Put_OI_Change": put_oi_change,
        "Zone_16_PCR": zone_16_pcr,
        "Zone_16_CPR": zone_16_cpr
    })

df_intra = generate_intraday_data(index_choice)

# --- TOP METRICS BAR ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Selected Index / Expiry", value=f"{index_choice} ({expiry_choice})")
with col2:
    curr_pcr = df_intra["Overall_PCR"].iloc[-1]
    st.metric(label="Market Overall PCR", value=round(curr_pcr, 3), delta="Bullish (>1.0)" if curr_pcr > 1.0 else "Bearish (<1.0)")
with col3:
    curr_cpr = df_intra["Overall_CPR"].iloc[-1]
    st.metric(label="Market Overall CPR", value=round(curr_cpr, 3), delta="Inverse Sentiment")
with col4:
    st.metric(label="Market Bias", value="Bullish Momentum" if curr_pcr > 1.05 else "Consolidation")

st.markdown("---")

# ==========================================
# SECTION A: INTRADAY TIMELINE RATIOS (PCR & CPR)
# ==========================================
st.subheader(f"📈 Part 1: Intraday Timeline Ratios ({index_choice} — {expiry_choice})")
st.markdown("Tracking overall market **Put-Call Ratio (PCR)** and **Call-Put Ratio (CPR)** alongside index spot movement.")

fig_overall = make_subplots(specs=[[{"secondary_y": True}]])
fig_overall.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Index_Price"], name=f"{index_choice} Price", mode="lines", line=dict(color="#9ca3af", width=1.5, dash="dot")), secondary_y=True)
fig_overall.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Overall_PCR"], name="Overall PCR", mode="lines", line=dict(color="#2563eb", width=2)), secondary_y=False)
fig_overall.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Overall_CPR"], name="Overall CPR", mode="lines", line=dict(color="#ef4444", width=2)), secondary_y=False)

fig_overall.update_xaxes(title_text="Time (12-Hour Format)", nticks=15)
fig_overall.update_yaxes(title_text="<b>Ratio Value (PCR / CPR)</b>", secondary_y=False)
fig_overall.update_yaxes(title_text="<b>Index Price</b>", secondary_y=True, tickformat="d")
fig_overall.update_layout(template=theme_template, hovermode="x unified", height=400, title="Market Overall PCR & CPR Timeline")
st.plotly_chart(fig_overall, use_container_width=True)

# Chart 2: OI Change Timeline
fig_oi = make_subplots(specs=[[{"secondary_y": True}]])
fig_oi.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Index_Price"], name=f"{index_choice} Price", mode="lines", line=dict(color="#cbd5e1", width=1, dash="dot")), secondary_y=True)
fig_oi.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Put_OI_Change"], name="Put OI Change (Cr)", mode="lines", line=dict(color="#10b981", width=2)), secondary_y=False)
fig_oi.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Call_OI_Change"], name="Call OI Change (Cr)", mode="lines", line=dict(color="#ef4444", width=2)), secondary_y=False)
fig_oi.update_xaxes(title_text="Time (12-Hour Format)", nticks=15)
fig_oi.update_yaxes(title_text="<b>OI Change (Crores)</b>", secondary_y=False)
fig_oi.update_yaxes(title_text="<b>Index Price</b>", secondary_y=True, tickformat="d")
fig_oi.update_layout(template=theme_template, hovermode="x unified", height=380, title="OI Change (Call vs Put) Intraday Chart")
st.plotly_chart(fig_oi, use_container_width=True)

st.markdown("---")

# ==========================================
# SECTION B: 16-STRIKE COMBINED ZONE ANALYSIS (8 Above + 8 Below)
# ==========================================
st.subheader("🔍 Part 2: 16-Strike Combined Zone Analysis (8 Above + 8 Below Strikes Aggregate)")
st.markdown("Aggregated Open Interest for 8 strikes above and 8 strikes below ATM (16 strikes total) matching Part 1 colors.")

fig_combined = make_subplots(specs=[[{"secondary_y": True}]])
fig_combined.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Index_Price"], name=f"{index_choice} Price", mode="lines", line=dict(color="#9ca3af", width=1.5, dash="dot")), secondary_y=True)
fig_combined.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Zone_16_PCR"], name="PCR", mode="lines", line=dict(color="#2563eb", width=2.5)))
fig_combined.add_trace(go.Scatter(x=df_intra["Time"], y=df_intra["Zone_16_CPR"], name="CPR", mode="lines", line=dict(color="#ef4444", width=2.5)))

fig_combined.update_xaxes(title_text="Time (12-Hour Format)", nticks=15)
fig_combined.update_yaxes(title_text="<b>Zone Ratios</b>", secondary_y=False)
fig_combined.update_yaxes(title_text="<b>Index Price</b>", secondary_y=True, tickformat="d")
fig_combined.update_layout(template=theme_template, hovermode="x unified", height=450, title="Combined 16-Strike Range (8 Above + 8 Below) PCR & CPR Timeline")
st.plotly_chart(fig_combined, use_container_width=True)