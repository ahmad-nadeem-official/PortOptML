import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Stock Price Viewer",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.title("Welcome to the Stock Dashboard")


results = yf.screen('most_actives')
top10 = results['quotes'][1:150]

currency = {
    "USD": "$",    
    "GBP": "£",    
    "EUR": "€",    
    "INR": "₹",    
    "CNY": "¥",    
    "JPY": "¥",    
    "CHF": "CHF",  
    "AED": "د.إ",  
    "SAR": "﷼",    
}


# Build the ticker line
ticker_items = []
for stock in top10:
    symbol = stock['symbol']
    price = stock['regularMarketPrice']
    change = stock['regularMarketChangePercent']
    curren = stock['currency']
    color = "green" if change >= 0 else "red"
    ticker_items.append(f"<span style='margin-right:40px'>{symbol}: {price:.2f}{currency[curren]}<span style='color:{color}'>({change:.2f}%)</span>|</span>")

ticker_line = " ".join(ticker_items)

st.markdown(
    f"""
    <style>
    .ticker {{
      width: 120%;
      overflow: hidden;
      white-space: nowrap;
      box-sizing: border-box;
    }}
    .ticker-text {{
      display: inline-block;
      padding-left: 100%;
      animation: ticker 39s linear infinite;
      font-size: 20px;
      font-family: monospace;
    }}
    @keyframes ticker {{
      0%   {{ transform: translateX(0%); }}
      100% {{ transform: translateX(-100%); }}
    }}
    
    </style>
    <div class="ticker">
      <div class="ticker-text">{ticker_line}</div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("<h3 style='color: #00F0A8;'>Choose your stock to get started</h3>", unsafe_allow_html=True)


@st.cache_data
def get_sp500():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    table = pd.read_html(response.text)[0]
    return table["Symbol"].tolist()


tickers = get_sp500()

if 'tick' not in st.session_state:
    st.session_state['tick'] = tickers[0]

st.sidebar.title("Settings")

stock_symbol = st.sidebar.selectbox("Enter Stock Symbol", tickers, index=tickers.index(st.session_state['tick']))
interval = st.sidebar.selectbox("Update Interval (seconds)", [10, 30, 60], index=1)
lookback = st.sidebar.selectbox("History Window", ["5m", "15m", "30m", "60m", "1d"], index=0)

st.sidebar.info("Data updates automatically")

# Create ticker object
ticker = yf.Ticker(stock_symbol)

# Session state to store data
if "prices" not in st.session_state:
    st.session_state.prices = pd.DataFrame()

# Function to fetch live price
def get_live_data(symbol, period="1d", interval="1m"):
    data = yf.download(tickers=symbol, period=period, interval=interval, progress=False)
    data = data[["Close"]].rename(columns={"Close": "Price"})
    return data

# Main live loop
placeholder = st.empty()


bg_color = st.get_option("theme.backgroundColor")

while True:
    try:
        live_data = get_live_data(stock_symbol, period="1d", interval="1m")
        live_data = live_data.tail(50)  # keep last 50 points for smooth graph

        # Merge with stored data
        st.session_state.prices = live_data

        # Display
        with placeholder.container():
            col1, col2 = st.columns([1, 2])

            # Latest price card
            with col1:
                latest_price = live_data["Price"].iloc[-1].item()
                prev_price = live_data["Price"].iloc[-2].item()
                change = ((latest_price - prev_price) / prev_price) * 100
                color = "green" if change >= 0 else "red"

                st.markdown(f"""
                <div style="padding:20px; border-radius:10px; color:white; text-align:center">
                    <h2>{stock_symbol}</h2>
                    <h1 style="color:{color};">${latest_price:.2f}</h1>
                    <p style="color:{color};">{change:.2f}% (last update)</p>
                </div>
                """, unsafe_allow_html=True)

            # Chart
            with col2:
                fig, ax = plt.subplots(figsize=(15,5))
                ax.plot(live_data.index, live_data["Price"], color='#008000', linewidth=2)
                ax.set_title(f"{stock_symbol} Live Price", fontsize=16)
                ax.set_xlabel("Time")
                ax.set_ylabel("Price (USD)")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

        time.sleep(interval)  # wait before next refresh

    except Exception as e:
        st.error(f"Error fetching live data: {e}")
        time.sleep(interval)
