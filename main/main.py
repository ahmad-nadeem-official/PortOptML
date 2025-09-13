import yfinance
import streamlit as st

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

