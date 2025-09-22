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


################################################# Portfolio Section #######################################
st.header("Portfolio Input")
st.write("Enter your stock portfolio details below. You can add multiple stocks along with their quantities.")


