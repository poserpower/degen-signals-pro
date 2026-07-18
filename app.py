import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Degen Signals Ultimate", page_icon="🔥", layout="wide")

# ====================== NEON DEGEN THEME ======================
st.markdown("""
<style>
    .main {background-color: #0a0a12;}
    h1, h2, h3 {color: #ff3366; text-shadow: 0 0 15px #ff3366;}
    .stTabs [data-baseweb="tab"] {background: linear-gradient(90deg, #1a1a2e, #2e1a2e); border-radius: 12px; color: #ffcc33; font-weight: bold;}
    .stTabs [aria-selected="true"] {background: linear-gradient(90deg, #ff3366, #ff6699) !important; color: white !important;}
    .metric-card {background: linear-gradient(145deg, #1a1a2e, #2e1a2e); padding: 18px; border-radius: 16px; border: 1px solid #ff336633; box-shadow: 0 4px 20px rgba(255, 51, 102, 0.15); transition: all 0.3s;}
    .metric-card:hover {transform: translateY(-5px); box-shadow: 0 8px 30px rgba(255, 51, 102, 0.3);}
</style>
""", unsafe_allow_html=True)

st.title("🔥 DEGEN SIGNALS ULTIMATE")
st.markdown("**Ultimate Alpha Terminal** — Stocks • Forex • Crypto • Memecoins • Smart Money • Whale Tracking • Alerts")

# ====================== EXPANDED ASSETS ======================
PRELOADED = {
    # MEMECOINS
    "PEPE": {"type": "memecoin", "price": 0.0000125, "change_pct": 15.3, "volume": 125000000, "avg_volume": 45000000, "ta_score": 62, "attention": 92, "catalyst": 45, "smart_money": 58, "notes": "Volume hype"},
    "WIF": {"type": "memecoin", "price": 2.45, "change_pct":