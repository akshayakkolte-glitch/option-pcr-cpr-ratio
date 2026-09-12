import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, time, timedelta

# Page Configuration
st.set_page_config(page_title="Option PCR & CPR Ratio", layout="wide")

# Top Header with Profile on the Right
header_left, header_right = st.columns([5, 1])

with header_left:
    st.title("📊 Option PCR & CPR Ratio: Real-Time Intraday Analytics")
    st.markdown("Professional derivatives intelligence tracking live timelines, overall market ratios, and 16-strike zone aggregation.")

with header_right:
    st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Akshay", width=40)
    st.markdown("**Akshay**")

st.markdown("---")

# Professional Top Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Strategy Builder", "Option Chain", "PCR & CPR Analytics", "Historical Chart"])

with tab1:
    st.header("Strategy Builder & Payoff Graphs")
    st.write("Build and analyze multi-leg option strategies with visual risk-reward profiles.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("📈 Short Straddle")
    with col2:
        st.info("📉 Short Strangle")
    with col3:
        st.info("🛡️ Short Iron Condor")
    with col4:
        st.info("🦋 Short Iron Butterfly")

with tab2:
    st.header("Live Option Chain")
    st.write("Real-time Open Interest (OI), change in OI, LTP, and strike prices.")
    
    # Mock Option Chain Table data
    option_chain_data = pd.DataFrame({
        "CALL OI": [150000, 230000, 410000, 890000, 1200000],
        "CALL Chg OI": [12000, -5000, 34000, 78000, 150000],
        "CALL LTP": [145.2, 98.5, 54.1, 22.4, 8.5],
        "Strike Price": [23300, 23350, 23400, 23450, 23500],
        "PUT LTP": [12.1, 28.4, 65.2, 112.0, 175.5],
        "PUT Chg OI": [-8000, 19000, 45000, 92000, 134000],
        "PUT OI": [900000, 750000, 620000, 410000, 210000]
    })
    st.dataframe(option_chain_data, use_container_width=True)

with tab3:
    # Sidebar Controls specific to analytics with dynamic expiry mapping
    st.sidebar.header("Dashboard Controls")
    index_choice = st.sidebar.selectbox("Select Index", ["NIFTY", "BANKNIFTY", "SENSEX"])
    
    # Dynamic expiry options based on selected index
    if index_choice == "NIFTY":
        expiry_options = ["15 Sep 2026", "22 Sep 2026", "29 Sep 2026"]
    elif index_choice == "BANKNIFTY":
        expiry_options = ["17 Sep 2026", "24 Sep 2026", "01 Oct 2026"]
    else:
        expiry_options = ["18 Sep 2026", "25 Sep 2026", "02 Oct 2026"]
        
    expiry_date = st.sidebar.selectbox("Select Expiry Date", expiry_options)
    chart_theme = st.sidebar.selectbox("Chart Theme", ["Dark", "Light"])

    # Summary metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Selected Index / Expiry", value=f"{index_choice} ({expiry_date})")
    with m2:
        st.metric(label="Market Overall PCR", value="0.955", delta="Bearish (<1.0)")
    with m3:
        st.metric(label="Market Overall CPR", value="1.046", delta="Inverse Sentiment")
    with m4:
        st.metric(label="Market Bias", value="Consolidation")

    st.markdown("---")
    st.subheader(f"Part 1: Intraday Timeline Ratios ({index_choice} — {expiry_date})")
    st.write("Tracking overall market Put-Call Ratio (PCR) and Call-Put Ratio (CPR) alongside index spot movement.")

    # Time series data generation with horizontal layout indices (Times on X-axis)
    times = pd.date_range("09:15", "15:30", freq="5min").time
    time_strs = [t.strftime("%I:%M %p") for t in times]
    
    np.random.seed(42)
    pcr_vals = np.clip(1.0 + np.cumsum(np.random.randn(len(times)) * 0.02), 0.8, 1.3)
    cpr_vals = np.clip(1.0 - np.cumsum(np.random.randn(len(times)) * 0.02), 0.7, 1.2)
    spot_vals = 23400 + np.cumsum(np.random.randn(len(times)) * 5)
    oi_change_call = np.cumsum(np.random.randn(len(times)) * 50)
    oi_change_put = np.cumsum(np.random.randn(len(times)) * 50)

    # Chart 1: Main PCR & CPR Timeline (Horizontal X-Axis, hovering shows both PCR and CPR)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=time_strs, y=pcr_vals, name="Overall PCR", mode="lines+markers", line=dict(color="blue", width=2)), secondary_y=False)
    fig.add_trace(go.Scatter(x=time_strs, y=cpr_vals, name="Overall CPR", mode="lines+markers", line=dict(color="red", width=2)), secondary_y=False)
    fig.add_trace(go.Scatter(x=time_strs, y=spot_vals, name=f"{index_choice} Price", mode="lines", line=dict(color="gray", width=1, dash="dash")), secondary_y=True)
    
    fig.update_layout(
        height=400, 
        margin=dict(l=20, r=20, t=20, b=20), 
        legend=dict(orientation="h", y=1.1, x=0.8),
        xaxis=dict(title="Time (Horizontal)")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Chart 2: OI Change Intraday Chart (Call vs Put Change)
    fig_oi = make_subplots(specs=[[{"secondary_y": True}]])
    fig_oi.add_trace(go.Scatter(x=time_strs, y=oi_change_call, name="Call OI Change", mode="lines", line=dict(color="red", width=2)), secondary_y=False)
    fig_oi.add_trace(go.Scatter(x=time_strs, y=oi_change_put, name="Put OI Change", mode="lines", line=dict(color="green", width=2)), secondary_y=False)
    fig_oi.add_trace(go.Scatter(x=time_strs, y=spot_vals, name=f"{index_choice} Price", mode="lines", line=dict(color="gray", width=1, dash="dash")), secondary_y=True)
    
    fig_oi.update_layout(
        height=300, 
        margin=dict(l=20, r=20, t=20, b=20), 
        legend=dict(orientation="h", y=1.1, x=0.8),
        xaxis=dict(title="Time (Horizontal)")
    )
    st.plotly_chart(fig_oi, use_container_width=True)

    st.markdown("---")
    st.subheader("Part 2: 16-Strike Combined Zone Analysis (8 Above + 8 Below Strikes Aggregate)")
    st.write(f"Aggregated Open Interest for 8 strikes above and 8 strikes below ATM ({index_choice}) matching Part 1 colors.")
    
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Scatter(x=time_strs, y=pcr_vals * 1.05, name="PCR", mode="lines", line=dict(color="blue", width=2)), secondary_y=False)
    fig2.add_trace(go.Scatter(x=time_strs, y=cpr_vals * 0.95, name="CPR", mode="lines", line=dict(color="red", width=2)), secondary_y=False)
    fig2.add_trace(go.Scatter(x=time_strs, y=spot_vals, name=f"{index_choice} Price", mode="lines", line=dict(color="gray", width=1, dash="dash")), secondary_y=True)
    
    fig2.update_layout(
        height=400, 
        margin=dict(l=20, r=20, t=20, b=20), 
        legend=dict(orientation="h", y=1.1, x=0.8),
        xaxis=dict(title="Time (Horizontal)")
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.header("Historical Charts & Market Depth")
    st.write("Analyze historical trends, volume profiles, and advance-decline indicators.")
