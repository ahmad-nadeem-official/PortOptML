import streamlit as st
import yfinance as yf


st.set_page_config(layout="wide")
# Get top 10 most active tickers from Yahoo
results = yf.screen('most_actives')
top10 = results['quotes'][:50]

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


logo = {
    'NVDA' : "https://logo.clearbit.com/nvidia.com"
}

# Build the ticker line
ticker_items = []
for stock in top10:
    symbol = stock['symbol']
    price = stock['regularMarketPrice']
    change = stock['regularMarketChangePercent']
    curren = stock['currency']
    color = "green" if change >= 0 else "red"
    ticker_items.append(f"<span style='margin-right:40px'>{symbol}: {price:.2f}{currency[curren]} <span style='color:{color}'>({change:.2f}%)</span></span>")

ticker_line = " ".join(ticker_items)

# Streamlit marquee-like effect
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
      animation: ticker 35s linear infinite;
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
