import yfinance as yf
import streamlit as st

st.title("Stock News")

# Use the ticker
# Make a Ticker object for Microsoft

msft = yf.Ticker("MSFT")

# Get the company's quarterly earnings (reported earnings vs expectations)
q_earnings = msft.quarterly_financials

st.write(q_earnings)
