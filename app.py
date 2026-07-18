import streamlit as st
import pandas as pd
import numpy as np
import requests
import yfinance as yf
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Degen Signals Ultimate", page_icon="🔥", layout="wide")

# ====================== NEON DEGEN THEME ======================
st.markdown("""
<style>
    .main {background-color: #0a0a12;}
    h1, h2, h3 {color: #ff3366; text-shadow: 0 0 15px #ff3366;}
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(90deg, #1a1a2e, #2e1a2e);
        border-radius: 12px;
        color: #ffcc33;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {background: linear-gradient(90deg, #ff3366, #ff6699) !important; color: white !important;}
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e, #2e1a2e);
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #ff336633;
        box-shadow: 0 4px 20px rgba(255, 51, 102, 0.15);
        transition: all 0.3s;
    }
    .metric-card:hover {transform: translateY(-5px); box-shadow: 0 8px 30px rgba(255, 51, 102, 0.3);}
</style>
""", unsafe_allow_html=True)

st.title("🔥 DEGEN SIGNALS ULTIMATE")
st.markdown("**The Ultimate Free Alpha Terminal** — Stocks • Forex • Crypto • Memecoins • Smart Money • Whale Tracking • Alerts")

# ====================== LARGE EXPANDED ASSET LIST ======================
PRELOADED = {
    # MEMECOINS
    "PEPE": {"type": "memecoin", "price": 0.0000125, "change_pct": 15.3, "volume": 125000000, "avg_volume": 45000000, "ta_score": 62, "attention": 92, "catalyst": 45, "smart_money": 58, "notes": "Volume hype"},
    "WIF": {"type": "memecoin", "price": 2.45, "change_pct": 8.7, "volume": 89000000, "avg_volume": 65000000, "ta_score": 68, "attention": 85, "catalyst": 50, "smart_money": 62, "notes": "dogwifhat"},
    "BONK": {"type": "memecoin", "price": 0.000028, "change_pct": -4.2, "volume": 89000000, "avg_volume": 120000000, "ta_score": 38, "attention": 58, "catalyst": 30, "smart_money": 42, "notes": "Solana OG"},
    "PENGU": {"type": "memecoin", "price": 0.0062, "change_pct": 5.2, "volume": 72000000, "avg_volume": 45000000, "ta_score": 71, "attention": 88, "catalyst": 65, "smart_money": 55, "notes": "Pudgy Penguins"},
    "FARTCOIN": {"type": "memecoin", "price": 0.149, "change_pct": 16.8, "volume": 58000000, "avg_volume": 32000000, "ta_score": 65, "attention": 95, "catalyst": 40, "smart_money": 48, "notes": "Viral AI"},
    "ANSEM": {"type": "memecoin", "price": 0.25, "change_pct": 20.5, "volume": 138000000, "avg_volume": 85000000, "ta_score": 78, "attention": 90, "catalyst": 55, "smart_money": 62, "notes": "Black Bull"},
    "POPCAT": {"type": "memecoin", "price": 0.85, "change_pct": 12.4, "volume": 65000000, "avg_volume": 42000000, "ta_score": 66, "attention": 82, "catalyst": 48, "smart_money": 51, "notes": "Cat leader"},
    "PNUT": {"type": "memecoin", "price": 0.42, "change_pct": 9.8, "volume": 48000000, "avg_volume": 31000000, "ta_score": 64, "attention": 87, "catalyst": 52, "smart_money": 55, "notes": "Peanut Squirrel"},
    "MOODENG": {"type": "memecoin", "price": 0.18, "change_pct": 18.2, "volume": 92000000, "avg_volume": 55000000, "ta_score": 72, "attention": 91, "catalyst": 58, "smart_money": 60, "notes": "High momentum"},
    "GIGA": {"type": "memecoin", "price": 0.032, "change_pct": 7.5, "volume": 38000000, "avg_volume": 28000000, "ta_score": 59, "attention": 78, "catalyst": 42, "smart_money": 48, "notes": "Gigachad"},
    "SPX6900": {"type": "memecoin", "price": 0.37, "change_pct": 8.7, "volume": 42000000, "avg_volume": 29000000, "ta_score": 67, "attention": 85, "catalyst": 55, "smart_money": 52, "notes": "S&P satire"},
    "BRETT": {"type": "memecoin", "price": 0.085, "change_pct": 11.2, "volume": 52000000, "avg_volume": 38000000, "ta_score": 64, "attention": 79, "catalyst": 48, "smart_money": 50, "notes": "Base meme"},
    "TROLL": {"type": "memecoin", "price": 0.055, "change_pct": 14.5, "volume": 68000000, "avg_volume": 45000000, "ta_score": 69, "attention": 88, "catalyst": 52, "smart_money": 55, "notes": "Trollface"},
    # CRYPTO
    "SOL": {"type": "crypto", "price": 145.3, "change_pct": 3.2, "volume": 2500000000, "avg_volume": 1800000000, "ta_score": 75, "attention": 80, "catalyst": 70, "smart_money": 68, "notes": "High performance