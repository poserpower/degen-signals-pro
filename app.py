import streamlit as st
import pandas as pd
import numpy as np
import requests
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta

# ====================== CONFIG & STYLING ======================
st.set_page_config(page_title="Degen Signals Ultimate", page_icon="🔥", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0a0e17;}
    h1, h2, h3 {color: #ff4b4b; font-family: 'Courier New', monospace;}
    .stTabs [data-baseweb="tab-list"] {gap: 20px;}
    .stTabs [data-baseweb="tab"] {
        background-color: #1a2338;
        border-radius: 12px;
        padding: 12px 28px;
        color: #ffaa00;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {background-color: #ff4b4b !important; color: white !important;}
    .metric-card {background-color: #1a2338; padding: 20px; border-radius: 12px; border: 1px solid #ff4b4b33;}
</style>
""", unsafe_allow_html=True)

st.title("🔥 DEGEN SIGNALS ULTIMATE")
st.markdown("**Pro + On-Chain + Live Memecoins + Backtesting** — The free alpha terminal")

# ====================== TABS ======================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 Dashboard", "📊 Live Memecoins", "📈 Pro Screener",
    "📰 News & Sentiment", "🐋 On-Chain Whales", "📉 Backtesting"
])

# (Keep all your existing functions: calculate_scores, get_signal, PRELOADED, etc.)
# Paste the rest of your original code here starting from the functions...

# Example for Dashboard tab with nicer cards:
with tab1:
    st.header("🚀 Main Signals Dashboard")
    items = []  # ... your original loop here ...
    df = pd.DataFrame(items).sort_values("Alpha Score", ascending=False)
    
    col1, col2, col3 = st.columns(3)
    for i, row in df.head(3).iterrows():
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{row['Symbol']}</h3>
                <h2 style="color:{'green' if row['Chg %'] > 0 else 'red'}">{row['Action']}</h2>
                <p>Alpha: <b>{row['Alpha Score']}</b></p>
            </div>
            """, unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True, hide_index=True)

# Add similar card styling to other tabs as needed