import streamlit as st
import pandas as pd
import numpy as np
import requests
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta

# ====================== PREMIUM DARK DEGEN THEME ======================
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
    .metric-card {
        background-color: #1a2338;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #ff4b4b33;
        margin-bottom: 12px;
        transition: transform 0.2s;
    }
    .metric-card:hover {transform: translateY(-4px);}
    .stDataFrame {background-color: #1a2338;}
    .quick-tool {
        background-color: #1a2338;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #ffaa0033;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔥 DEGEN SIGNALS ULTIMATE")
st.markdown("**Pro + On-Chain + Live Memecoins + Backtesting** — The free alpha terminal • Updated just now")

# ====================== EXPANDED ASSETS (Coins + Stocks) ======================
PRELOADED = {
    # Memecoins (expanded)
    "PEPE": {"type": "memecoin", "price": 0.0000125, "change_pct": 15.3, "volume": 125000000, "avg_volume": 45000000,
             "ta_score": 62, "attention_score": 92, "catalyst_score": 45, "smart_money_score": 58, "notes": "Volume anomaly + hype"},
    "WIF": {"type": "memecoin", "price": 2.45, "change_pct": 8.7, "volume": 89000000, "avg_volume": 65000000,
            "ta_score": 68, "attention_score": 85, "catalyst_score": 50, "smart_money_score": 62, "notes": "dogwifhat momentum"},
    "BONK": {"type": "memecoin", "price": 0.000028, "change_pct": -4.2, "volume": 89000000, "avg_volume": 120000000,
             "ta_score": 38, "attention_score": 58, "catalyst_score": 30, "smart_money_score": 42, "notes": "Cooling signals"},
    "PENGU": {"type": "memecoin", "price": 0.0062, "change_pct": 5.2, "volume": 72000000, "avg_volume": 45000000,
              "ta_score": 71, "attention_score": 88, "catalyst_score": 65, "smart_money_score": 55, "notes": "Pudgy Penguins brand"},
    "FARTCOIN": {"type": "memecoin", "price": 0.149, "change_pct": 16.8, "volume": 58000000, "avg_volume": 32000000,
                 "ta_score": 65, "attention_score": 95, "catalyst_score": 40, "smart_money_score": 48, "notes": "Viral AI humor"},
    "ANSEM": {"type": "memecoin", "price": 0.25, "change_pct": 20.5, "volume": 138000000, "avg_volume": 85000000,
              "ta_score": 78, "attention_score": 90, "catalyst_score": 55, "smart_money_score": 62, "notes": "Black Bull momentum"},
    # Major Crypto
    "SOL": {"type": "crypto", "price": 145.3, "change_pct": 3.2, "volume": 2500000000, "avg_volume": 1800000000,
            "ta_score": 75, "attention_score": 80, "catalyst_score": 70, "smart_money_score": 68, "notes": "Ecosystem strength"},
    "BTC": {"type": "crypto", "price": 64200, "change_pct": 2.8, "volume": 42000000000, "avg_volume": 38000000000,
            "ta_score": 82, "attention_score": 75, "catalyst_score": 60, "smart_money_score": 78, "notes": "Digital gold"},
    "ETH": {"type": "crypto", "price": 3180, "change_pct": 4.1, "volume": 18000000000, "avg_volume": 15000000000,
            "ta_score": 79, "attention_score": 72, "catalyst_score": 65, "smart_money_score": 70, "notes": "Smart contracts leader"},
    # Stocks & Crypto Stocks
    "NVDA": {"type": "stock", "price": 120.5, "change_pct": 1.8, "volume": 45000000, "avg_volume": 38000000,
             "ta_score": 82, "attention_score": 78, "catalyst_score": 85, "smart_money_score": 80, "notes": "AI leader"},
    "AMD": {"type": "stock", "price": 550.25, "change_pct": 2.1, "volume": 28500000, "avg_volume": 22000000,
            "ta_score": 78, "attention_score": 65, "catalyst_score": 90, "smart_money_score": 72, "notes": "AI event + earnings"},
    "MSTR": {"type": "stock", "price": 94.64, "change_pct": 0.8, "volume": 15000000, "avg_volume": 12000000,
             "ta_score": 85, "attention_score": 92, "catalyst_score": 75, "smart_money_score": 88, "notes": "Bitcoin treasury play"},
    "COIN": {"type": "stock", "price": 159.07, "change_pct": 2.05, "volume": 9680000, "avg_volume": 8500000,
             "ta_score": 76, "attention_score": 70, "catalyst_score": 68, "smart_money_score": 65, "notes": "Crypto exchange leader"},
    "HOOD": {"type": "stock", "price": 111.97, "change_pct": 4.28, "volume": 30000000, "avg_volume": 25000000,
             "ta_score": 74, "attention_score": 68, "catalyst_score": 72, "smart_money_score": 60, "notes": "Retail + prediction markets"},
    "TSLA": {"type": "stock", "price": 248.5, "change_pct": -1.2, "volume": 95000000, "avg_volume": 82000000,
             "ta_score": 68, "attention_score": 85, "catalyst_score": 55, "smart_money_score": 58, "notes": "Elon + robotaxi hype"},
}

# ====================== FUNCTIONS ======================
def calculate_scores(data):
    vol = data.get("volume", 0)
    avg_vol = max(data.get("avg_volume", 1), 1)
    rvol = vol / avg_vol
    anomaly = 95 if rvol >= 3 else (80 if rvol >= 2 else (65 if rvol >= 1.5 else 40))
    momentum = min(100, data.get("ta_score", 50) * 0.6 + min(100, abs(data.get("change_pct", 0)) * 8) * 0.2 + anomaly * 0.2)
    total = (0.25 * min(100, (rvol / 2) * 70 + min(30, np.log10(max(vol, 1)) * 3)) +
             0.20 * anomaly + 0.20 * momentum +
             0.15 * data.get("attention_score", 50) + 0.10 * data.get("catalyst_score", 50) +
             0.10 * data.get("smart_money_score", 50))
    return {
        "anomaly": round(anomaly, 1), "momentum": round(momentum, 1),
        "attention": data.get("attention_score", 50), "catalyst": data.get("catalyst_score", 50),
        "smart_money": data.get("smart_money_score", 50),
        "alpha_score": round(total, 1), "rvol": round(rvol, 2)
    }

def get_signal(scores, change_pct):
    alpha = scores["alpha_score"]
    anom = scores["anomaly"]
    mom = scores["momentum"]
    if alpha >= 80 and anom >= 80 and mom >= 70 and change_pct > 0:
        return "🟢 STRONG BUY", "Highest early confluence"
    elif alpha >= 65 and anom >= 70:
        return "🟡 BUY / ACCUMULATE", "Volume + momentum building"
    elif alpha <= 40 or (change_pct < -5 and scores["rvol"] >= 2):
        return "🔴 SELL / AVOID", "Distribution forming"
    else:
        return "⚪ WATCH", "Monitoring"

# ====================== TABS ======================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 Dashboard", "📊 Live Memecoins", "📈 Pro Screener",
    "📰 News & Sentiment", "🐋 On-Chain Whales", "📉 Backtesting"
])

# ====================== TAB 1: ENHANCED DASHBOARD (HOME) ======================
with tab1:
    # Top bar
    colA, colB = st.columns([3, 1])
    with colA:
        st.header("🚀 Live Alpha Dashboard")
    with colB:
        if st.button("🔄 Refresh Data"):
            st.rerun()

    # Quick Stats
    st.subheader("📊 Quick Stats")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Total Assets Tracked", len(PRELOADED))
    q2.metric("High Alpha Signals", len([s for s in PRELOADED.values() if calculate_scores(s)["alpha_score"] > 70]))
    q3.metric("Avg Alpha Score", round(np.mean([calculate_scores(d)["alpha_score"] for d in PRELOADED.values()]), 1))
    q