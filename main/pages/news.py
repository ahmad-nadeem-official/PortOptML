import feedparser
import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time


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

choice = st.selectbox("Choose a stock to get its news", tickers, index=tickers.index(st.session_state['tick']))
st.session_state['tick'] = choice

warning_h = st.empty()
warning_h.warning("News might take a while to load, please be patient...")
time.sleep(3)  # wait 3 seconds

# Replace with second warning
warning_h.warning("Refresh might shuffle the news order, please be patient...")


st.set_page_config(layout="wide")
st.title("Latest News about your favorite stocks")


ticker = st.session_state['tick']
url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
feed = feedparser.parse(url)

for entry in feed.entries[:10]:
    title = entry.title
    link = entry.link
    
    # Some feeds include image in media_content or media_thumbnail
    image = None
    if "media_content" in entry:
        image = entry.media_content[0]['url']
    elif "media_thumbnail" in entry:
        image = entry.media_thumbnail[0]['url']
    
    st.write(title)
    st.write("Link:", link)
    st.write("Image:", image)
    st.write("-" * 50)


st.markdown(
    """
    <div style="background-color:#fff3cd; padding:10px; border-radius:10px; color:#856404;">
    ⚠️ <b>Disclaimer:</b> Stock prices and news may be delayed or inaccurate. 
    This tool is for <b>educational purposes only</b> and not investment advice.
    </div>
    """, 
    unsafe_allow_html=True
)    