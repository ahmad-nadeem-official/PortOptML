import streamlit as st
import yfinance as yf
import pandas as pd
import requests


st.set_page_config(layout="wide")
st.sidebar.title("TRADMINCER v1.02")

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

st.success(f"record of 1 year of {st.session_state['tick']} fetched successfully!")
st.write(data)



# --- 4. Display the graph ---
st.subheader(f"{st.session_state['tick']} Price Chart (Last 1 Year)")
# st.line_chart(data['Close'])
# st.line_chart(data['Volume'])
st.line_chart(data[['Open', 'High', 'Low', 'Close']])

tick_s = st.session_state['tick']
tick = yf.Ticker(tick_s)

st.write(tick.quarterly_income_stmt)

# '''extra inof'''
meta = tick.info

company = meta['longName']
st.markdown(f"<h3>The business summary of <span style='color:#00F0A8;'>{company}</span></h3>", unsafe_allow_html=True)
st.write(meta['longBusinessSummary'])
 
st.subheader("Key Information")
col1, col2 = st.columns(2)

# {meta['city']}, {meta['state']}, 

with col1:
    st.write(f"**Address:** {meta['address1']}, {meta['zip']}, {meta['country']}")
    st.write(f"**Sector:** {meta['sector']}")
    st.write(f"**Industry:** {meta['industry']}")
    st.write(f"**Website:** {meta['website']}")
    st.write(f"**Phone:** {meta['phone']}")
    st.write(f"**Current Price:** {meta['currentPrice']:.2f} {meta['currentPrice']}")
    st.write(f"**Market Cap:** {meta['marketCap']:,} {meta['currency']}")
    st.write(f"**52 Week High:** {meta['fiftyTwoWeekHigh']:.2f} {meta['currency']}")
    st.write(f"**52 Week Low:** {meta['fiftyTwoWeekLow']:.2f} {meta['currency']}")
    st.write(f"**Average Volume:** {meta['averageVolume']:,}")

with col2:
    st.write(f"**Previous Close:** {meta['previousClose']:.2f} {meta['currency']}")
    st.write(f"**Open:** {meta['open']:.2f} {meta['currency']}")
    st.write(f"**Day's Range:** {meta['dayLow']:.2f} - {meta['dayHigh']:.2f} {meta['currency']}")
    st.write(f"**Volume:** {meta['volume']:,}")
    st.write(f"**Dividend Yield:** {meta.get('dividendYield', 'N/A')}")
    st.write(f"**Ex-Dividend Date:** {meta.get('exDividendDate', 'N/A')}")
    st.write(f"**1y Target Est:** {meta.get('targetMeanPrice', 'N/A')} {meta['currency']}")
    st.write(f"**Beta:** {meta['beta']}")
    st.write(f"**PE Ratio (TTM):** {meta.get('trailingPE', 'N/A')}")
    st.write(f"**EPS (TTM):** {meta.get('trailingEps', 'N/A')}")


st.markdown(f"<span style='color:#00F0A8;'>Shares History of {company}</span>", unsafe_allow_html=True)

ticker_obj = yf.Ticker(st.session_state['tick'])

dates = st.date_input(
    "Select Date Range",
    value=(pd.to_datetime("2023-01-01"), pd.to_datetime("today")),
    min_value=pd.to_datetime("2000-01-01"),
    max_value=pd.to_datetime("today")
)

start_date, end_date = dates
shares = ticker_obj.history(start=start_date, end=end_date)

cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']

st.subheader(f"{company} — History From ({start_date} to {end_date})")
st.subheader("Price (OHLC)")
st.line_chart(shares[['Open', 'High', 'Low', 'Close']], use_container_width=True)

st.subheader("Volume")
st.line_chart(shares[['Volume']], use_container_width=True)

st.subheader("Dividends & Stock Splits")
st.line_chart(shares[['Dividends', 'Stock Splits']], use_container_width=True)

st.markdown(f"<span style='color:#00F0A8;'>Major Shareholders of {company}</span>", unsafe_allow_html=True)

# Create a Ticker object for Apple
m_h = yf.Ticker(st.session_state['tick'])

# Get major shareholders
holders = m_h.get_major_holders()
st.dataframe(holders)
