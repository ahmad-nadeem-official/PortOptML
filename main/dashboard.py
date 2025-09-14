import yfinance as yf
import streamlit as st
import xgboost as xgb

st.set_page_config(
    page_title="Stock Price Viewer",
    page_icon=":chart_with_upwards_trend:",
)

st.title("Stock Price Viewer")
st.sidebar.file_uploader("")


# if "ticker" not in st.session_state:
#     st.session_state["ticker"] = "AAPL"

if 'say' not in st.session_state:
    st.session_state['say'] = ""


isay = st.text_input("Enter Stock Ticker", st.session_state['say'])
st.session_state['say'] = isay

if isay:
    st.write(f"You entered: {st.session_state['say']}")


# Use the ticker
ticker = "AAPL"

# New API for news
news = yf.get_yf_rss(ticker)[:10]  # returns a list of dicts

for i, item in enumerate(news):
    st.subheader(f"{i+1}. {item['title']}")
    st.write(item['link'])
    st.write(item['publisher'])
    st.write(item['providerPublishTime'])
    st.write("---")    

