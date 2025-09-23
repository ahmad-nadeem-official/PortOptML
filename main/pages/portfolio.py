import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

st.set_page_config(layout="wide")
st.sidebar.title("TRADMINCER v1.02")

######################################## Sidebar #######################################
st.sidebar.markdown(
    """
    <h3 style="
        background: linear-gradient(to right, #ff0000, #ff4d4d, #ff9999);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 5px #ff0000, 0 0 10px #ff4d4d, 0 0 20px #ff0000;
        animation: pulse 1.5s infinite;
    ">
        ⚠️ This is not financial advice. For educational purposes only ⚠️
    </h3>
    <style>
    @keyframes pulse {
        0% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff4d4d, 0 0 20px #ff0000; }
        50% { text-shadow: 0 0 20px #ff4d4d, 0 0 30px #ff0000, 0 0 40px #ff4d4d; }
        100% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff4d4d, 0 0 20px #ff0000; }
    }
    </style>
    """,
    unsafe_allow_html=True
)



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


st.title("Portfolio Optimization and Analysis")
st.write("This page allows you to analyze and optimize your stock portfolio using various financial metrics and visualization tools.")

st.markdown("<h3 style='color: #00F0A8;'>Choose your stock to get started</h3>", unsafe_allow_html=True)

############################################## stock Data Fetching #######################################
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





################################################# Portfolio Section #######################################
st.header("Portfolio Input")
st.write("Enter your stock portfolio details below. You can add multiple stocks along with their quantities.")

st.sidebar.header("Add Stock to Portfolio")


if "list" not in st.session_state:
    st.session_state["list"] = []

if "quant" not in st.session_state:
    st.session_state["quant"] = []



with st.sidebar.form("portfolio_form", clear_on_submit=True):
    stock_symbol = st.selectbox(
        "Enter Stock Symbol", tickers, index=tickers.index(st.session_state["tick"])
    )


    stock_quantity = st.number_input("Quantity", min_value=1, value=10)
    
    submit_button = st.form_submit_button("Add to Portfolio")

    if submit_button:
        st.session_state["list"].append(stock_symbol)
        st.session_state["quant"].append(stock_quantity)

# ✅ Build dataframe after updates
new_data = pd.DataFrame({
    "stocks": st.session_state["list"],
    "quantity": st.session_state["quant"]
})

st.dataframe(new_data, use_container_width=True)

st.sidebar.info("Form will be refresh once you added a stock and its quantity")
st.sidebar.info("If you refresh the page, all data will be lost")




