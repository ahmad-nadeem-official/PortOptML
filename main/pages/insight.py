import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt


favicon_path = "/home/muhammad-ahmad-nadeem/Projects/PortOptML/main/Tradmincer.png"
st.set_page_config(
    page_icon=favicon_path,
    page_title="Stock Price Viewer",
    layout="wide",
)


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


# st.title("Welcome to the world of Finance")
st.markdown("<h3 style='color: #00F0A8;'>Choose your stock to get Insights</h3>", unsafe_allow_html=True)


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

ticker = st.session_state['tick']

st.title(f"{ticker} Analyst Recommendations")

data = yf.Ticker(ticker)
recs = data.get_recommendations()

# Keep last 6 rows (6 months)
recs = recs.tail(10).reset_index(drop=True)

# Show table
st.subheader("Analyst Recommendations for last few months")
st.dataframe(recs)

# Stacked bar chart
st.subheader("Analyst Sentiment Trend")

fig, ax = plt.subplots(figsize=(8, 5))
recs.set_index("period")[["strongBuy", "buy", "hold", "sell", "strongSell"]].plot(kind="bar", stacked=True,ax=ax)

ax.set_ylabel("Number of Analysts")
ax.set_xlabel("Period")
ax.set_title(f"{ticker} Analyst Ratings Over Time")
st.pyplot(fig)

# Consensus summary
latest = recs.iloc[-1]
buy_score = latest["strongBuy"] + latest["buy"]
sell_score = latest["sell"] + latest["strongSell"]

if buy_score > sell_score:
    consensus = "BUY"
elif sell_score > buy_score:
    consensus = "SELL"
else:
    consensus = "HOLD"

st.subheader("Consensus (Latest Period)")
st.write(
    f"Strong Buy + Buy = {buy_score} | Hold = {latest['hold']} | Sell + Strong Sell = {sell_score}"
)
st.success(f"Overall Consensus: {consensus}")