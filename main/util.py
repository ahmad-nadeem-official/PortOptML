import yfinance as yf
import pandas as pd

POPULAR_TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'V', 'WMT',
    'JNJ', 'UNH', 'HD', 'PG', 'MA', 'BAC', 'PFE', 'KO', 'PEP', 'DIS',
    'NFLX', 'ADBE', 'CRM', 'INTC', 'CSCO', 'VZ', 'T', 'XOM', 'CVX',
    'BA', 'GE', 'F', 'GM', 'AMD', 'QCOM', 'TXN', 'MU', 'LRCX', 'AMAT'
]


def get_most_active():
    """Replacement for yf.screen('most_actives') which was removed in newer yfinance."""
    # auto_adjust is pinned explicitly: yfinance is changing this default, and
    # leaving it implicit makes the prices shift between library versions.
    data = yf.download(POPULAR_TICKERS, period="1d", progress=False,
                       group_by='ticker', auto_adjust=True)
    quotes = []
    for symbol in POPULAR_TICKERS:
        try:
            if len(POPULAR_TICKERS) > 1:
                stock_data = data[symbol]
            else:
                stock_data = data
            if not stock_data.empty:
                price = float(stock_data['Close'].iloc[-1])
                prev_close = float(stock_data['Open'].iloc[0]) if len(stock_data) > 0 else price
                change_pct = ((price - prev_close) / prev_close) * 100 if prev_close else 0
                quotes.append({
                    'symbol': symbol,
                    'regularMarketPrice': price,
                    'regularMarketChangePercent': change_pct,
                    'currency': 'USD'
                })
        except Exception:
            continue
    return {'quotes': quotes}


if __name__ == "__main__":
    import cv2
    image = cv2.imread("Tradmincer_big.png")
    resized_image = cv2.resize(image, (2024, 2024), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite("main/Tradmincer_big2.png", resized_image)
    print("Image resized and saved as main/Tradmincer_big2.png")
