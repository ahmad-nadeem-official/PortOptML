import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
import time
from scipy.optimize import minimize
import plotly.express as px
import matplotlib.cm as cm


st.set_page_config(
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
    )


st.sidebar.title("TRADMINCER v1.02")

######################################## Sidebar #######################################
st.sidebar.markdown(
    """
    <h3 style="
        background: linear-gradient(to right, #ff0000, #ff4d4d, #ff9999);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 5px #ff0000, 0 0 10px #ff4d4d, 0 0 20px #ff0000;
        animation: pulse 1.5s infinite;
    ">
        ⚠️ This is not financial advice. For educational purposes only ⚠️
    </h3>
    <style>
    @keyframes pulse {
        0% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff4d4d, 0 0 20px #ff0000; }
        50% { text-shadow: 0 0 20px #ff4d4d, 0 0 30px #ff0000, 0 0 40px #ff4d4d; }
        100% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff4d4d, 0 0 20px #ff0000; }
    }
    </style>
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


st.title("Portfolio Optimization and Analysis")
st.write("This page allows you to analyze and optimize your stock portfolio using various financial metrics and visualization tools.")

st.markdown("<h3 style='color: #00F0A8;'>Choose your stock to get started</h3>", unsafe_allow_html=True)

############################################## stock Data Fetching #######################################
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

################################################# Portfolio Section #######################################
st.header("Portfolio Analysis and Optimization")
st.write("See your stock portfolio details below. You can add multiple stocks along with their quantities.")

st.sidebar.header("Add Stock to Portfolio")


if "list" not in st.session_state:
    st.session_state["list"] = []

if "quant" not in st.session_state:
    st.session_state["quant"] = []

if "price" not in st.session_state:
    st.session_state["price"] = []

if 'u_price' not in st.session_state:
    st.session_state['u_price'] = [] 

with st.sidebar.form("portfolio_form", clear_on_submit=True):
    stock_symbol = st.selectbox(
        "Enter Stock Symbol", tickers, index=tickers.index(st.session_state["tick"])
    )
    stock_quantity = st.number_input("Quantity", min_value=1, value=10)

    ticker = yf.Ticker(stock_symbol)
    u_price = ticker.fast_info['last_price']
    price = u_price * stock_quantity
    
    # st.write("Live Price (fast):", price)


    submit_button = st.form_submit_button("Add to Portfolio")

    if submit_button:
        if stock_symbol in st.session_state["list"]:
          st.sidebar.error(f"{stock_symbol} already added! choose another stock")
        else:
         st.session_state["list"].append(stock_symbol)
         st.session_state["quant"].append(stock_quantity)
         st.session_state["price"].append(price)
         st.session_state['u_price'].append(u_price)

# ✅ Build dataframe after updates
new_data = pd.DataFrame({
    "stocks": st.session_state["list"],
    "quantity": st.session_state["quant"],
    "price" : st.session_state["price"],
    "unit_price": st.session_state['u_price']
})

st.dataframe(new_data, use_container_width=True)

st.sidebar.info("Form will be refresh once you added a stock and its quantity")
st.sidebar.info("If you refresh the page, all data will be lost")

# def get_live_data(symbol):
#     data = yf.download(tickers=symbol, period="1d", interval="1m", progress=False)
#     if data.empty:
#         return pd.DataFrame(columns=["Price"])
#     return data[["Close"]].rename(columns={"Close": "Price"})

# live_data = get_live_data(stock_symbol).tail(50)


##########################################portfolio Analysis ##########################################
st.header("Portfolio Analysis")

today = date.today()

if new_data.empty:
    st.warning("Please add stocks to your portfolio to see the analysis.")
    st.stop()


data = yf.download(new_data['stocks'].tolist(), start="2015-01-01", end=today)
data = data['Close']
st.line_chart(data,x_label="last 10 years till now", y_label="stock prices", use_container_width=True)

if len(new_data["stocks"]) < 2:
    st.warning("Please add at least two different stocks to your portfolio for analysis")
    st.stop()

# if new_data["stocks"].duplicated().any():
#     st.error("Duplicate stock symbols detected! Please remove duplicates before proceeding.")
#     col = st.selectbox("Select a stock to remove", new_data["stocks"].tolist())
#     new_data = new_data[new_data["stocks"] != col]  # Remove selected stock
#     for col in ["stocks", "price", "quant", "u_price"]:
#      if col in st.session_state:
#         del st.session_state[col]
#     st.stop()

returns = data.pct_change().dropna()

mean_returns = returns.mean()
cov_matrix = returns.cov()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Mean Returns")
    st.success(f"Mean returns calculated successfully! {mean_returns.shape[0]}")
    
with col2:
    st.subheader("Covariance Matrix")
    st.write(cov_matrix)

################################## Portfolio Simulation/ wieghts ##########################################

num_assets = len(new_data['stocks'])

# Step 4: Portfolio performance function
def portfolio_performance(weights):
    ret = np.dot(weights, mean_returns) * 252  # annualized return
    vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))  # annualized volatility
    sharpe = ret / vol
    return ret, vol, sharpe

# Step 5: Objective -> minimize negative Sharpe (maximize Sharpe)
def neg_sharpe(weights):
    return -portfolio_performance(weights)[2]

# Step 6: Constraints (sum of weights = 1)
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0, 1) for asset in range(num_assets))
init_guess = num_assets * [1. / num_assets]

# Step 7: Optimization
opt_results = minimize(neg_sharpe, init_guess, bounds=bounds, constraints=constraints)
opt_weights = opt_results.x

coll1, coll2 = st.columns(2)




with coll1:
  st.subheader("Optimal Portfolio Weights")
  for stock, weight in zip(new_data['stocks'], opt_weights):
      st.markdown(
          f"<span style='color: #00FF00; font-weight: bold'>{stock}</span>: "
          f"<b>{weight:.2%}</b>",
          unsafe_allow_html=True
      )
      data = pd.Series([stock], index=[weight])  

with coll2:
   colors = cm.tab20(np.linspace(0, 1, len(new_data['stocks'])))
   fig, ax = plt.subplots()
   ax.pie(
       opt_weights,
       labels=new_data['stocks'],
       autopct='%1.1f%%',
       startangle=140,
       colors=colors
   )
   ax.axis('equal')  # Equal aspect ratio ensures the pie is a circle
   st.pyplot(fig)


ret, vol, sharpe = portfolio_performance(opt_weights)

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Annual Return")
    st.success(f"{ret:.2%}")
with col2:
    st.subheader("Volatility")
    st.success(f"{vol:.2%}")
with col3:
    st.subheader("Sharpe Ratio")
    st.success(f"{sharpe:.2f}")