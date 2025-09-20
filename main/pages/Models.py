import streamlit as st
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta, date
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, root_mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Stock Price Prediction Models",
    page_icon=":crystal_ball:",
    layout="wide",
)
st.markdown("<p style='color: #474955; font-size:50px; font-weight:bold;'>Stock Price Predictor</p>",unsafe_allow_html=True)

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


st.markdown("<h3 style='color: #00F0A8;'>Choose your stock to get started</h3>", unsafe_allow_html=True)


################################### tickers getting Functions #######################################
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

stock_symbol = st.selectbox("Enter Stock Symbol", tickers, index=tickers.index(st.session_state['tick']))
st.session_state['tick'] = stock_symbol


######################################### Ticker Tape #######################################
tick = yf.Ticker(st.session_state['tick'])
meta = tick.info

day = date.today()

data = yf.download(st.session_state['tick'], start="2015-01-01", end=day, progress=False)
st.markdown(f"<h4 style='color: #db4237;'>Record of Last 10 years of {meta['longName']}</h4>", unsafe_allow_html=True)
st.dataframe(data)


######################################## Feature adding #######################################
data['Return'] = data['Close'].pct_change()  # target
data['MA10'] = data['Close'].rolling(10).mean()
data['MA50'] = data['Close'].rolling(50).mean()
data['Volatility'] = data['Return'].rolling(20).std()
data = data.dropna()
st.success("Features added successfully!")
st.write(data.head(5))

######################################## Train test Splitting ####################################
features = ['Open','High','Low','Close','Volume','MA10','MA50','Volatility']

x = data[features]
y = data['Return']

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42, shuffle=False)
st.write(f"Training samples: {x_train.shape[0]}, Testing samples: {x_test.shape[0]}")


##################################### scalling ##############################################
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(x_train)
X_test_scaled = scaler.fit_transform(x_test)

st.success("Data Scaled successfully!")

##################################### Model Training ########################################
model_xgb = xgb.XGBRegressor(
    booster='gbtree',             # Booster type ('gbtree', 'gblinear', or 'dart')
    n_jobs=4,                     # Parallel threads; -1 uses all cores.
    random_state=42,              # Random seed for reproducibility.
    verbosity=1,                  # Output verbosity.
    
    n_estimators=500,             # Number of boosting rounds.
    learning_rate=0.05,           # Step size shrinkage.
    max_depth=5,                  # Maximum tree depth.
    min_child_weight=1,           # Minimum sum of instance weight in a child node.
    gamma=0.2,                    # Minimum loss reduction for a split.
    subsample=0.8,                # Subsample ratio of training instances.
    colsample_bytree=0.8,         # Subsample ratio of columns per tree.
    reg_alpha=0.1,                # L1 regularization.
    reg_lambda=1,                 # L2 regularization.
    
    objective='reg:squarederror', # Learning objective (e.g., regression with squared loss).
    eval_metric='rmse'            # Evaluation metric.
)

model_rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='auto',
    random_state=42,
    oob_score=True,
    bootstrap=False,
    n_jobs=-1
)

model_knn = KNeighborsRegressor(
    n_neighbors=5,
    weights='uniform',
    algorithm='auto',
    leaf_size=30,
    p=2,
    metric='minkowski',
    n_jobs=-1
)

model_knn.fit(X_train_scaled, y_train)
st.success("Model Trained successfully on KNN!")

model_rf.fit(X_train_scaled, y_train)
st.success("Model Trained successfully on Random Forest!")


model_xgb.fit(X_train_scaled, y_train)
st.success("Model Trained successfully on XGBoost!")





##################################### Model Evaluation ########################################
y_pred_xgb = model_xgb.predict(X_test_scaled)
y_pred_rf = model_rf.predict(X_test_scaled)
y_pred_knn = model_knn.predict(X_test_scaled)


rmse = root_mean_squared_error(y_test, y_pred_xgb)
st.success(f"RMSE -- XGB: {rmse:.6f}")

mse = mean_squared_error(y_test, y_pred_rf)
st.success(f"RMSE -- RF: {mse:.6f}")

mae = mean_absolute_error(y_test, y_pred_knn)
st.success(f"RMSE -- KNN: {mae:.6f}")