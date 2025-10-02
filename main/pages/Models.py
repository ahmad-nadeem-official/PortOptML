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

favicon_path = "main/Tradmincer_big.png"
st.set_page_config(
    page_icon=favicon_path,
    page_title="Tradmincer",
    layout="wide",
)


st.sidebar.title("TRADMINCER v1.02")

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
st.info("for your exposure, we are showing you only top 10 rows of the dataset")
st.write(data.head(10))

######################################## Train test Splitting ####################################
features = ['Open','High','Low','Close','Volume','MA10','MA50','Volatility']

x = data[features]
y = data['Return']

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42, shuffle=False)
st.write(f"Training samples: {x_train.shape[0]}, Testing samples: {x_test.shape[0]}")


##################################### scalling ##############################################
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(x_train)
X_test_scaled = scaler.transform(x_test)

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
    max_features=5,
    random_state=42,
    oob_score=True,
    bootstrap=True,
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

if y_pred_xgb not in st.session_state:
    st.session_state['y_pred_xgb'] = y_pred_xgb
if y_pred_rf not in st.session_state:
    st.session_state['y_pred_rf'] = y_pred_rf
if y_pred_knn not in st.session_state:
    st.session_state['y_pred_knn'] = y_pred_knn





rmse = root_mean_squared_error(y_test, y_pred_xgb)
mse = mean_squared_error(y_test, y_pred_rf)
mae = mean_absolute_error(y_test, y_pred_knn)
#################################### session state for model eval #############################
if 'model_xgb' not in st.session_state:
    st.session_state['model_xgb'] = rmse
if 'model_rf' not in st.session_state:
    st.session_state['model_rf'] = mse
if 'model_knn' not in st.session_state:
    st.session_state['model_knn'] = mae

###################################### Visualization ########################################
# st.markdown("<h3 style='color: #00F0A8;'>Model Predictions vs Actual Returns</h3>", unsafe_allow_html=True)
# plt.figure(figsize=(14,7))
# plt.plot(y_test.index, y_test, label='Actual Returns', color='blue')
# plt.plot(y_test.index, y_pred_xgb, label='XGBoost Predictions', color='red', alpha=0.7)
# plt.plot(y_test.index, y_pred_rf, label='Random Forest Predictions', color='green', alpha=0.7)
# plt.plot(y_test.index, y_pred_knn, label='KNN Predictions', color='orange', alpha=0.7)
# plt.xlabel('Date')
# plt.ylabel('Returns')
# plt.title(f'{meta["longName"]} Returns Prediction')
# plt.legend()
# plt.grid()
# st.pyplot(plt)
# plt.clf()

st.subheader("Model Evaluation Metrics")
coli1, coli2, coli3 = st.columns(3)      

with coli1:
    st.subheader("XGBoost")
    st.success(f"RMSE -- XGB: {st.session_state['model_xgb']:.6f}")

with coli2:
    st.subheader("Random Forest")
    st.success(f"MSE -- RF: {st.session_state['model_rf']:.6f}")

with coli3:
    st.subheader("KNN")
    st.success(f"MAE -- KNN: {st.session_state['model_knn']:.6f}")  

####################################### Streamlit version #######################################
pred_df = pd.DataFrame({
    'Actual Returns': y_test.values,
    'XGBoost Predictions': st.session_state['y_pred_xgb'],
    'Random Forest Predictions': st.session_state['y_pred_rf'],
    'KNN Predictions': st.session_state['y_pred_knn']
}, index=y_test.index)

st.markdown("<h3 style='color: #00F0A8;'>Model Predictions vs Actual Returns</h3>", unsafe_allow_html=True)
st.line_chart(pred_df)

st.info(f"Now the models have trained on {stock_symbol} stock data, you can predict future returns by entering future stock data in the sidebar and clicking the 'Predict Future Returns' button.")

####################################### Initialize session_state #################################
if 'open_price' not in st.session_state:
    st.session_state['open_price'] = float(data['Open'].iloc[-1])
if 'high_price' not in st.session_state:
    st.session_state['high_price'] = float(data['High'].iloc[-1])
if 'low_price' not in st.session_state:
    st.session_state['low_price'] = float(data['Low'].iloc[-1])
if 'close_price' not in st.session_state:
    st.session_state['close_price'] = float(data['Close'].iloc[-1])
if 'volume' not in st.session_state:
    st.session_state['volume'] = int(data['Volume'].iloc[-1])

####################################### Future Prediction Sidebar #################################
st.sidebar.header("Enter future stock data")


with st.sidebar.form("future_form"):
    st.markdown("<h3 style='color: #edd040;'>Future Price Prediction</h3>", unsafe_allow_html=True)

    open_price = st.number_input("Open Price", value=st.session_state.get("open_price", 0.0))
    high_price = st.number_input("High Price", value=st.session_state.get("high_price", 0.0))
    low_price = st.number_input("Low Price", value=st.session_state.get("low_price", 0.0))
    close_price = st.number_input("Close Price", value=st.session_state.get("close_price", 0.0))
    volume = st.number_input("Volume", value=st.session_state.get("volume", 0))

    # submitted = st.form_submit_button("Add Data")

    # if submitted :
    st.session_state['open_price'] = open_price
    st.session_state['high_price'] = high_price
    st.session_state['low_price'] = low_price
    st.session_state['close_price'] = close_price
    st.session_state['volume'] = volume


    # Compute moving averages and volatility from recent historical data
    ma10 = data['Close'].rolling(10).mean().iloc[-1]
    ma50 = data['Close'].rolling(50).mean().iloc[-1]
    volatility = data['Return'].rolling(20).std().iloc[-1]

    # Prepare feature vector
    future_features = pd.DataFrame({
        'Open': [open_price],
        'High': [high_price],
        'Low': [low_price],
        'Close': [close_price],
        'Volume': [volume],
        'MA10': [ma10],
        'MA50': [ma50],
        'Volatility': [volatility]
    })

    # Scale features
    future_scaled = scaler.transform(future_features)
    
    # Predict returns
    but = st.form_submit_button("Predict Future Returns")
    if not but:
        st.stop()

    st.info("After predicting one time the form will return to past values")


pred_xgb = model_xgb.predict(future_scaled)[0]
pred_rf = model_rf.predict(future_scaled)[0]
pred_knn = model_knn.predict(future_scaled)[0]

st.markdown("<h3 style='color: #00F0A8;'>Predicted Future Returns</h3>", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"XGBoost: {pred_xgb:.6f}")
with col2:
    st.info(f"Random Forest: {pred_rf:.6f}")
with col3:
    st.info(f"KNN: {pred_knn:.6f}")

   



    
    
    
    


