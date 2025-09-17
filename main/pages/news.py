# import streamlit as st
# import requests
# from bs4 import BeautifulSoup

# url = "https://finance.yahoo.com/quote/NVDA/news"
# headers = {"User-Agent": "Mozilla/5.0"}
# r = requests.get(url, headers=headers)
# soup = BeautifulSoup(r.text, "html.parser")

# for item in soup.find_all('h3'):
#     print(item.text)



# st.markdown("<h1 style='color: #3a8ec2;' text-align='center'>This is currently under-develop page</h1>", unsafe_allow_html=True)

import yfinance as yf
print(yf.__version__)
