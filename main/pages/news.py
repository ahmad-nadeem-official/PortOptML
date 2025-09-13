import yfinance as yf
import streamlit as st

st.title("Stock News")

# Use the ticker
# Make a Ticker object for Microsoft


col1, col2 = st.columns(2)

with col1:

   msft = yf.Ticker("MSFT")
   
   # Get the company's quarterly earnings (reported earnings vs expectations)
   q_earnings = msft.quarterly_financials
   
   st.write(q_earnings)


with col2:
   st.image("https://s.yimg.com/cv/apiv2/social/images/yahoo_default_logo.png")
   # Create a Ticker object for Microsoft
   msft = yf.Ticker("MSFT")
   
   # Get the company's quarterly financial statements (Income Statement)
   q_financials = msft.quarterly_financials
   
   st.write(q_financials)