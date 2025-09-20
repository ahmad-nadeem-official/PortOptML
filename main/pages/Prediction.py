import streamlit as st
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta, date
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Stock Price Prediction",
    page_icon=":crystal_ball:",
    layout="wide",
)
st.markdown("<p style='color: #474955; font-size:50px; font-weight:bold;'>Stock Price Predictor</p>",unsafe_allow_html=True)

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


st.markdown("<h3 style='color: #00F0A8;'>Choose your stock to get started</h3>", unsafe_allow_html=True)


################################### tickers getting Functions #######################################
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

stock_symbol = st.selectbox("Enter Stock Symbol", tickers, index=tickers.index(st.session_state['tick']))
st.session_state['tick'] = stock_symbol


######################################### Ticker Tape #######################################
tick = yf.Ticker(stock_symbol)

day = date.today()

data = yf.download(st.session_state['tick'], start="2015-01-01", end=day, progress=False)
st.dataframe(data)