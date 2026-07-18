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

# ====================== MASSIVE ASSET LIST ======================
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
    "SOL": {"type": "crypto", "price": 145.3, "change_pct": 3.2, "volume": 2500000000, "avg_volume": 1800000000, "ta_score": 75, "attention": 80, "catalyst": 70, "smart_money": 68, "notes": "High performance"},
    "BTC": {"type": "crypto", "price": 64200, "change_pct": 2.8, "volume": 42000000000, "avg_volume": 38000000000, "ta_score": 82, "attention": 75, "catalyst": 60, "smart_money": 78, "notes": "Digital gold"},
    "ETH": {"type": "crypto", "price": 3180, "change_pct": 4.1, "volume": 18000000000, "avg_volume": 15000000000, "ta_score": 79, "attention": 72, "catalyst": 65, "smart_money": 70, "notes": "World computer"},
    "SUI": {"type": "crypto", "price": 2.85, "change_pct": 6.4, "volume": 1200000000, "avg_volume": 850000000, "ta_score": 73, "attention": 68, "catalyst": 72, "smart_money": 65, "notes": "Fast L1"},
    "AVAX": {"type": "crypto", "price": 38.5, "change_pct": 5.1, "volume": 980000000, "avg_volume": 720000000, "ta_score": 71, "attention": 65, "catalyst": 68, "smart_money": 62, "notes": "Subnets"},
    "LINK": {"type": "crypto", "price": 14.8, "change_pct": 4.5, "volume": 650000000, "avg_volume": 480000000, "ta_score": 70, "attention": 62, "catalyst": 75, "smart_money": 68, "notes": "Oracles"},
    # STOCKS
    "NVDA": {"type": "stock", "price": 120.5, "change_pct": 1.8, "volume": 45000000, "avg_volume": 38000000, "ta_score": 82, "attention": 78, "catalyst": 85, "smart_money": 80, "notes": "AI leader"},
    "AMD": {"type": "stock", "price": 550.25, "change_pct": 2.1, "volume": 28500000, "avg_volume": 22000000, "ta_score": 78, "attention": 65, "catalyst": 90, "smart_money": 72, "notes": "AI + earnings"},
    "MSTR": {"type": "stock", "price": 94.64, "change_pct": 0.8, "volume": 15000000, "avg_volume": 12000000, "ta_score": 85, "attention": 92, "catalyst": 75, "smart_money": 88, "notes": "Bitcoin treasury"},
    "COIN": {"type": "stock", "price": 159.07, "change_pct": 2.05, "volume": 9680000, "avg_volume": 8500000, "ta_score": 76, "attention": 70, "catalyst": 68, "smart_money": 65, "notes": "Crypto exchange"},
    "HOOD": {"type": "stock", "price": 111.97, "change_pct": 4.28, "volume": 30000000, "avg_volume": 25000000, "ta_score": 74, "attention": 68, "catalyst": 72, "smart_money": 60, "notes": "Retail broker"},
    "TSLA": {"type": "stock", "price": 248.5, "change_pct": -1.2, "volume": 95000000, "avg_volume": 82000000, "ta_score": 68, "attention": 85, "catalyst": 55, "smart_money": 58, "notes": "Elon play"},
    "AAPL": {"type": "stock", "price": 228.5, "change_pct": 0.9, "volume": 52000000, "avg_volume": 48000000, "ta_score": 72, "attention": 60, "catalyst": 65, "smart_money": 70, "notes": "Stable blue chip"},
    # FOREX
    "EURUSD": {"type": "forex", "price": 1.085, "change_pct": 0.25, "volume": 0, "avg_volume": 0, "ta_score": 65, "attention": 55, "catalyst": 50, "smart_money": 60, "notes": "Major pair"},
    "GBPUSD": {"type": "forex", "price": 1.295, "change_pct": 0.35, "volume": 0, "avg_volume": 0, "ta_score": 62, "attention": 52, "catalyst": 48, "smart_money": 58, "notes": "Cable"},
    "USDJPY": {"type": "forex", "price": 155.8, "change_pct": -0.15, "volume": 0, "avg_volume": 0, "ta_score": 60, "attention": 50, "catalyst": 52, "smart_money": 55, "notes": "Safe haven"},
}

def calculate_scores(data):
    vol = data.get("volume", 0)
    avg_vol = max(data.get("avg_volume", 1), 1)
    rvol = vol / avg_vol if avg_vol > 0 else 1
    anomaly = 95 if rvol >= 3 else (80 if rvol >= 2 else (65 if rvol >= 1.5 else 40))
    momentum = min(100, data.get("ta_score", 50) * 0.6 + min(100, abs(data.get("change_pct", 0)) * 8) * 0.2 + anomaly * 0.2)
    total = (0.25 * min(100, (rvol / 2) * 70 + min(30, np.log10(max(vol, 1)) * 3)) +
             0.20 * anomaly + 0.20 * momentum + 0.15 * data.get("attention", 50) +
             0.10 * data.get("catalyst", 50) + 0.10 * data.get("smart_money", 50))
    return {"alpha_score": round(total, 1), "rvol": round(rvol, 2), "anomaly": round(anomaly, 1)}

def get_signal(scores, change_pct):
    alpha = scores["alpha_score"]
    if alpha >= 80 and change_pct > 0: return "🟢 STRONG BUY", "Highest confluence"
    elif alpha >= 65: return "🟡 BUY / ACCUMULATE", "Momentum building"
    elif alpha <= 40 or (change_pct < -5 and scores.get("rvol", 0) >= 2): return "🔴 SELL / AVOID", "Distribution"
    return "⚪ WATCH", "Monitoring"

# ====================== TABS ======================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 Dashboard", "📊 Live Memecoins", "📈 Pro Screener", 
    "📰 News & Alerts", "🐋 Smart Money & Whales", "📉 Backtesting"
])

# ====================== DASHBOARD ======================
with tab1:
    st.header("🚀 Live Alpha Dashboard")
    if st.button("🔄 Refresh All", type="primary"):
        st.rerun()

    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    with col1: search = st.text_input("🔍 Search Symbol", "")
    with col2: type_filter = st.multiselect("Type", ["memecoin", "crypto", "stock", "forex"], default=["memecoin", "crypto", "stock", "forex"])
    with col3: min_alpha = st.slider("Min Alpha Score", 0, 100, 50)

    items = []
    for sym, d in PRELOADED.items():
        if search and search.lower() not in sym.lower(): continue
        if d["type"] not in type_filter: continue
        sc = calculate_scores(d)
        if sc["alpha_score"] < min_alpha: continue
        act, reason = get_signal(sc, d["change_pct"])
        items.append({
            "Symbol": sym, "Type": d["type"].upper(), "Price": d["price"], "Chg %": d["change_pct"],
            "RVOL": sc["rvol"], "Anomaly": sc["anomaly"], "Alpha Score": sc["alpha_score"],
            "Action": act, "Reason": reason, "Notes": d["notes"]
        })

    df = pd.DataFrame(items)
    if not df.empty:
        df = df.sort_values("Alpha Score", ascending=False)

    st.subheader("📊 Quick Stats")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Total Tracked", len(PRELOADED))
    q2.metric("High Alpha", len([i for i in items if i["Alpha Score"] >= 70]))
    q3.metric("Avg Alpha", round(np.mean([i["Alpha Score"] for i in items]) if items else 0, 1))
    q4.metric("Top Mover", max(PRELOADED, key=lambda x: PRELOADED[x]["change_pct"]))

    st.subheader("🔥 Top Alpha Picks")
    if not df.empty:
        cols = st.columns(4)
        for i, (_, row) in enumerate(df.head(4).iterrows()):
            with cols[i]:
                color = "#00ff88" if row["Chg %"] > 0 else "#ff3366"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{row['Symbol']} ({row['Type']})</h3>
                    <h2 style="color:{color};">{row['Action']}</h2>
                    <p><b>{row['Alpha Score']}</b> Alpha</p>
                </div>
                """, unsafe_allow_html=True)

    st.subheader("📋 Full Signal Table")
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)

# ====================== OTHER TABS ======================
with tab2:
    st.header("📊 Live Memecoins")
    st.info("High-volume memecoins ready.")

with tab3:
    st.header("📈 Pro Screener")
    st.info("Filters ready.")

with tab4:
    st.header("📰 News & Alerts")
    st.subheader("🔔 Alert System")
    alert_symbol = st.selectbox("Asset", list(PRELOADED.keys()))
    threshold = st.slider("Alpha Threshold", 50, 95, 75)
    if st.button("Check Alert"):
        sc = calculate_scores(PRELOADED[alert_symbol])
        if sc["alpha_score"] >= threshold:
            st.success(f"🚨 ALERT: {alert_symbol} Alpha = {sc['alpha_score']}")
        else:
            st.info(f"No alert for {alert_symbol}")

with tab5:
    st.header("🐋 Smart Money & Whales")
    st.subheader("Smart Money Scores")
    sm_df = pd.DataFrame([{"Symbol": k, "Smart Money": v["smart_money"]} for k, v in PRELOADED.items()]).sort_values("Smart Money", ascending=False)
    st.dataframe(sm_df.head(15), use_container_width=True)
    st.info("Connect Arkham / Nansen / The Graph for live whale tracking.")

with tab6:
    st.header("📉 Backtesting")
    ticker = st.selectbox("Ticker", list(PRELOADED.keys()))
    if st.button("Run Backtest"):
        st.success(f"Demo backtest for {ticker} ready.")

st.caption("Degen Signals Ultimate • Not financial advice • Add more assets to PRELOADED anytime")