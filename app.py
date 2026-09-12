import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, time, timedelta

# Page Configuration
st.set_page_config(page_title="Option PCR & CPR Ratio", layout="wide")

# Top Header without Profile section
st.title("📊 Option PCR & CPR Ratio: Real-Time Intraday Analytics")
st.markdown("Professional derivatives intelligence tracking live timelines, overall market ratios, and 16-strike zone aggregation.")

st.markdown("---")

# --- GLOBAL SIDEBAR CONTROLS & AUTO-REFRESH TOGGLE ---
st.sidebar.header("Dashboard Controls")
index_choice = st.sidebar.selectbox("Select Index", ["NIFTY", "BANKNIFTY", "SENSEX"])

if index_choice == "NIFTY":
    expiry_options = ["15 Sep 2026", "22 Sep 2026", "29 Sep 2026"]
elif index_choice == "BANKNIFTY":
    expiry_options = ["15 Sep 2026", "22 Sep 2026", "29 Sep 2026"]
else:  # SENSEX
    expiry_options = ["17 Sep 2026", "24 Sep 2026", "01 Oct 2026"]
    
expiry_date = st.sidebar.selectbox("Select Expiry Date", expiry_options)
chart_theme = st.sidebar.selectbox("Chart Theme", ["Dark", "Light"])

st.sidebar.markdown("---")
st.sidebar.subheader("Live Feed Status")
auto_refresh = st.sidebar.toggle("🟢 Auto-Refresh (Live)", value=True)

if auto_refresh:
    st.sidebar.caption("Status: **Active (Live Feed ON)**")
else:
    st.sidebar.caption("Status: **Paused (Manual Mode)**")

# Dynamic metric labels based on selected index
pcr_label = f"{index_choice} Overall PCR"
cpr_label = f"{index_choice} Overall CPR"

# --- MAIN ANALYTICS DASHBOARD (Single View, No Tabs) ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="Selected Index / Expiry", value=f"{index_choice} ({expiry_date})")
with m2:
    st.metric(label=pcr_label, value="0.94", delta="Bearish (<1.0)")
with m3:
    st.metric(label=cpr_label, value="1.064", delta="Inverse Sentiment")
with m4:
    st.metric(label="Market Bias", value="Consolidation")

st.markdown("---")
st.subheader(f"Part 1: Intraday Timeline Ratios ({index_choice} — {expiry_date})")
st.write(f"Tracking {index_choice} live session data from market open up to the current time.")

# Generate full day 1-min sequence from 09:15 to 15:30
full_times = pd.date_range("2026-09-12 09:15:00", "2026-09-12 15:30:00", freq="1min")

# Dynamic check: match current system time to simulate live market progression
now_time = datetime.now().time()
market_open = time(9, 15)
market_close = time(15, 30)

# For testing or outside market hours, default to full view or slice up to current time
# If market is ongoing, slice data up to the current minute
active_end_index = len(full_times)
if market_open <= now_time <= market_close:
    # Find matching index for current time
    current_dt = datetime.combine(datetime.today(), now_time)
    # Filter full_times up to current time
    valid_times = [t for t in full_times if t.time() <= now_time]
    if len(valid_times) > 0:
        active_end_index = len(valid_times)

times = full_times[:active_end_index]
time_strs = [t.strftime("%I:%M %p") for t in times]

# Set tick marks at every 30-minute interval for clean axis display
tick_indices = list(range(0, len(time_strs), 30))
tick_vals = [time_strs[i] for i in tick_indices if i < len(time_strs)]

np.random.seed(42)
num_points = len(times)
pcr_vals = np.clip(1.0 + np.cumsum(np.random.randn(num_points) * 0.01), 0.8, 1.3)
cpr_vals = np.clip(1.0 - np.cumsum(np.random.randn(num_points) * 0.01), 0.7, 1.2)
spot_vals = 76800 + np.cumsum(np.random.randn(num_points) * 2)
oi_change_call = np.cumsum(np.random.randn(num_points) * 20)
oi_change_put = np.cumsum(np.random.randn(num_points) * 20)

# Chart 1: Main PCR & CPR Timeline
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=time_strs, y=pcr_vals, name="Overall PCR", mode="lines", line=dict(color="blue", width=2)), secondary_y=False)
fig.add_trace(go.Scatter(x=time_strs, y=cpr_vals, name="Overall CPR", mode="lines", line=dict(color="red", width=2)), secondary_y=False)
fig.add_trace(go.Scatter(x=time_strs, y=spot_vals, name=f"{index_choice} Price", mode="lines", line=dict(color="gray", width=1, dash="dash")), secondary_y=True)

fig.update_layout(
    height=400, 
    margin=dict(l=20, r=20, t=20, b=20), 
    legend=dict(orientation="h", y=1.1, x=0.8), 
    hovermode="x unified", 
    xaxis=dict(tickmode='array', tickvals=tick_vals, tickangle=0)
)
st.plotly_chart(fig, use_container_width=True)

# Chart 2: OI Change Intraday Chart
fig_oi = make_subplots(specs=[[{"secondary_y": True}]])
fig_oi.add_trace(go.Scatter(x=time_strs, y=oi_change_call, name="Call OI Change", mode="lines", line=dict(color="red", width=2)), secondary_y=False)
fig_oi.add_trace(go.Scatter(x=time_strs, y=oi_change_put, name="Put OI Change", mode="lines", line=dict(color="green", width=2)), secondary_y=False)
fig_oi.add_trace(go.Scatter(x=time_strs, y=spot_vals, name=f"{index_choice} Price", mode="lines", line=dict(color="gray", width=1, dash="dash")), secondary_y=True)

fig_oi.update_layout(
    height=300, 
    margin=dict(l=20, r=20, t=20, b=20), 
    legend=dict(orientation="h", y=1.1, x=0.8), 
    hovermode="x unified", 
    xaxis=dict(tickmode='array', tickvals=tick_vals, tickangle=0)
)
st.plotly_chart(fig_oi, use_container_width=True)

st.markdown("---")
st.subheader("Part 2: 16-Strike Combined Zone Analysis (8 Above + 8 Below Strikes Aggregate)")
st.write(f"Aggregated Open Interest for 8 strikes above and 8 strikes below ATM ({index_choice}).")

fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(go.Scatter(x=time_strs, y=pcr_vals * 1.05, name="PCR", mode="lines", line=dict(color="blue", width=2)), secondary_y=False)
fig2.add_trace(go.Scatter(x=time_strs, y=cpr_vals * 0.95, name="CPR", mode="lines", line=dict(color="red", width=2)), secondary_y=False)
fig2.add_trace(go.Scatter(x=time_strs, y=spot_vals, name=f"{index_choice} Price", mode="lines", line=dict(color="gray", width=1, dash="dash")), secondary_y=True)

fig2.update_layout(
    height=400, 
    margin=dict(l=20, r=20, t=20, b=20), 
    legend=dict(orientation="h", y=1.1, x=0.8), 
    hovermode="x unified", 
    xaxis=dict(tickmode='array', tickvals=tick_vals, tickangle=0)
)
st.plotly_chart(fig2, use_container_width=True)
