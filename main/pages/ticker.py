import streamlit as st
import yfinance as yf
import pandas as pd
import requests


st.set_page_config(layout="wide")

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


st.title("Welcome to the world of Finance")
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

choice = st.selectbox("Choose a stock", tickers, index=tickers.index(st.session_state['tick']))
st.session_state['tick'] = choice

# --- 3. Fetch historical data for selected ticker ---
@st.cache_data
def get_stock_data(ticker):
    data = yf.Ticker(ticker).history(period="1y")  # last 1 year
    return data

data = get_stock_data(st.session_state['tick'])

st.write(data)



# --- 4. Display the graph ---
st.subheader(f"{st.session_state['tick']} Price Chart (Last 1 Year)")
# st.line_chart(data['Close'])
# st.line_chart(data['Volume'])
st.line_chart(data[['Open', 'High', 'Low', 'Close']])

tick_s = st.session_state['tick']
tick = yf.Ticker(tick_s)

st.write(tick.quarterly_income_stmt)
