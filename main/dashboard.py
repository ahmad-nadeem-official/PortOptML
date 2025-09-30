import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time
import darkdetect
from datetime import datetime, timedelta


try :
    st.set_page_config(
        page_title="Stock Price Viewer",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
    )
    
    st.sidebar.title("TRADMINCER v1.02")
    st.title("Welcome to the Stock Dashboard")
    
    st.sidebar.markdown(
        """
        <div style="background-color:#fff3cd; padding:10px; border-radius:10px; color:#856404;">
         <b>Disclaimer:</b> Stock prices and news may be delayed or inaccurate. 
        This tool is for <b>educational purposes only</b> and not investment advice.
        </div>
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
    interval = "1m"
    period =  "1d"
    
    st.sidebar.info("Data updates automatically")
    
    # Create ticker object
    ticker = yf.Ticker(stock_symbol)
    
    # Session state to store data
    if "prices" not in st.session_state:
        st.session_state.prices = pd.DataFrame()
    
    # Function to fetch live price
    def get_live_data(symbol):
        data = yf.download(tickers=symbol, period=period, interval=interval, progress=False)
        if data.empty:
            return pd.DataFrame(columns=["Price"])
        return data[["Close"]].rename(columns={"Close": "Price"})
        
    
    # Main live loop
    #remember the white board example
    placeholder = st.empty()
    warning_h = st.empty()
    
    #bg of system
    bg_color = st.get_option("theme.backgroundColor")
    
    while True:
        try:
            live_data = get_live_data(stock_symbol).tail(50) # fetch last 50 data points for smooth graph
    
            # Merge with stored data
            st.session_state.prices = live_data
    
            # changes whole compund at a time
            with placeholder.container():
                col1, col2 = st.columns([1, 2])
    
                # Latest price card
                with col1:
    
                    # .iloc[-1] still gives you a Pandas object (Series element).
                    # .item() converts it into a plain Python number (like float or int).
                    
    
                    #this loop is to check whether we have enough data points
                    if len(live_data) >= 2:
                        latest_price = live_data["Price"].iloc[-1].item()
                        prev_price   = live_data["Price"].iloc[-2].item()
                        warning_h.empty()  # ✅ clear warning when we have data
                    elif len(live_data) == 1:
                        latest_price = live_data["Price"].iloc[-1].item()
                        prev_price   = latest_price   
                        warning_h.empty()  # ✅ also clear warning
                    else:
                        latest_price = None
                        prev_price   = None
                        warning_h.warning("Please restart the app")  # ✅ show warning
                        continue
    
                    #change formula
                    change = ((latest_price - prev_price) / prev_price) * 100
                    color = "green" if change >= 0 else "red"
                    
    
                    # fixed inline style strings
                    if darkdetect.isDark():
                        st.markdown(
                            f"""
                            <div style="padding:20px; border-radius:10px; text-align:center"><h1 color:white;>{stock_symbol}</h1>
                            <h1 style="color:{color};">${latest_price:.2f}</h1>
                            <p style="color:{color};">{change:.2f}% (last update)</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                             <div style="padding:20px; border-radius:10px; text-align:center;">
                             <h1 style="color:##a0a0a0;">{stock_symbol}<h1>
                              <h1 style="color:{color};">${latest_price:.2f}</h1>
                              <p style="color:{color};">{change:.2f}% (last update)</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
    
    
                # Chart
                with col2:
                   fig, ax = plt.subplots(figsize=(15,5))
                   ax.plot(live_data.index, live_data["Price"], color='#00FF00', linewidth=2)  # brighter green
                   
                   ax.set_title(f"{stock_symbol} Live Price", fontsize=16)
                   ax.set_xlabel("Time")
                   ax.set_ylabel("Price (USD)")
                   
                   # Detect system theme
                   if darkdetect.isDark():
                       # Title + labels white
                       ax.set_title(f"{stock_symbol} Live Price", fontsize=16, color="white")
                       ax.set_xlabel("Time", color="white")
                       ax.set_ylabel("Price (USD)", color="white")
                   
                       # Make ticks white
                       ax.tick_params(colors="white")
                   
                       # Grid lines gray
                       ax.grid(True, alpha=0.3, color="gray")
                   
                       # Transparent background
                       fig.patch.set_alpha(0)
                       ax.patch.set_alpha(0)
                   
                   else:
                       # Light mode adjustments (optional)
                       ax.grid(True, alpha=0.3, color="black")
                   
                   # ✅ No transparent=True here
                   st.pyplot(fig)
    
    
            time.sleep(30)  # wait before next refresh
    
        except Exception as e:
            st.error(f"Error fetching live data: {e}")
            time.sleep(30)
except Exception as e:
    st.error(f"Error in app: {e}")





