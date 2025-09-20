import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Stock Price Prediction",
    page_icon=":crystal_ball:",
    layout="wide",
)

st.markdown(
    "<p style='color: #474955; font-size:50px; font-weight:bold;'>Stock Price Predictor</p>", 
    unsafe_allow_html=True
)

st.sidebar.header("This is not financial advice. For educational purposes only")