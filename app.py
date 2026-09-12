import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, time, timedelta

# Page Configuration for Wide Layout
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

# Professional Top Navigation Tabs (Like Groww, Kite, and StockMojo)
tab1, tab2, tab3, tab4 = st.tabs(["Strategy Builder", "Option Chain", "PCR & CPR Analytics", "Historical Chart"])

with tab1:
    st.header("Strategy Builder & Payoff Graphs")
    st.write("Build and analyze multi-leg option strategies with visual risk-reward profiles.")
    
    # Sample layout columns for ready-made strategies
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
    st.success("Option chain table and strike visualization will display here.")

with tab3:
    st.header("Real-Time Intraday Analytics (PCR & CPR)")
    
    # Sidebar Controls specific to analytics
    st.sidebar.header("Dashboard Controls")
    index_choice = st.sidebar.selectbox("Select Index", ["NIFTY", "BANKNIFTY", "SENSEX"])
    expiry_date = st.sidebar.selectbox("Select Expiry Date", ["15 Sep 2026", "22 Sep 2026", "29 Sep 2026"])
    chart_theme = st.sidebar.selectbox("Chart Theme", ["Dark", "Light"])

    # Summary metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label=f"Selected Index / Expiry", value=f"{index_choice} ({expiry_date})")
    with m2:
        st.metric(label="Market Overall PCR", value="1.424", delta="Bullish (+1.0)")
    with m3:
        st.metric(label="Market Overall CPR", value="0.705", delta="Inverse Sentiment")
    with m4:
        st.metric(label="Market Bias", value="Bullish Momentum")

    st.markdown("---")
    st.subheader(f"Part 1: Intraday Timeline Ratios ({index_choice} — {expiry_date})")
    st.write("Tracking overall market Put-Call Ratio (PCR) and Call-Put Ratio (CPR) alongside index spot movement.")

    # Sample chart placeholder
    chart_data = pd.DataFrame(
        np.random.randn(20, 2) * 0.1 + 1.2,
        columns=["Overall PCR", "Overall CPR"]
    )
    st.line_chart(chart_data)

with tab4:
    st.header("Historical Charts & Market Depth")
    st.write("Analyze historical trends, volume profiles, and advance-decline indicators.")
