TRADMINCER: Advanced Stock Market Dashboard
===========================================

Failed to load image

[View link](https://via.placeholder.com/1200x300?text=TRADMINCER+v1.02)

_(Replace with actual banner image for visual appeal)_

Overview
--------

TRADMINCER is a comprehensive, interactive web application built with Streamlit for real-time stock market analysis, portfolio optimization, and predictive modeling. Designed for finance enthusiasts, traders, and data scientists, it leverages APIs like Yahoo Finance (yfinance) to fetch live data, perform machine learning-based predictions, and provide actionable insights. This project demonstrates proficiency in full-stack data applications, from data ingestion and ETL to ML model deployment and user-friendly UI/UX.

Key highlights:

*   **Real-time Data Integration**: Fetches and visualizes live stock prices, news, and analyst recommendations.
*   **Machine Learning Models**: Implements regression models (XGBoost, Random Forest, KNN) for stock return predictions.
*   **Portfolio Optimization**: Uses Modern Portfolio Theory (MPT) with SciPy optimization for efficient frontier analysis.
*   **Responsive Design**: Supports dark/light mode detection and wide layouts for enhanced user experience.

This project showcases my skills in Python-based data engineering, machine learning, and web development, making it a strong portfolio piece for roles in fintech, data science, or software engineering at leading companies like Google, Amazon, or JPMorgan Chase.

Features
--------

*   **Live Ticker Tape**: Displays real-time prices and percentage changes for the most active stocks using a scrolling marquee.
*   **Stock Insights**: Analyst recommendations, sentiment trends, and consensus ratings with visualizations (stacked bar charts).
*   **Predictive Modeling**: Trains ML models on historical data to forecast stock returns; supports user-input future data for predictions.
*   **News Feed**: Aggregates latest RSS news headlines for selected stocks, including images and links.
*   **Portfolio Management**: Allows users to build portfolios, compute optimal weights using Sharpe Ratio maximization, and visualize allocations (pie charts).
*   **Historical Data Viewer**: Interactive charts for OHLC, volume, dividends, and stock splits over custom date ranges.
*   **Dashboard**: Real-time price monitoring with dynamic charts, auto-refresh, and theme-aware styling.
*   **S&P 500 Integration**: Automatically fetches and lists all S&P 500 tickers for easy selection.
*   **Error Handling & Caching**: Uses Streamlit's caching for performance; includes disclaimers for educational use.

Tech Stack
----------

*   **Frontend/Backend**:![Streamlit](https://img.shields.io/badge/Streamlit-1.0-FF4B4B?logo=streamlit&logoColor=white) Streamlit (for rapid prototyping and deployment)
*   **Data Fetching**: ![yfinance](https://img.shields.io/badge/yfinance-6001d2?logo=yahoo&logoColor=white)
 (Yahoo Finance API), requests, feedparser (RSS parsing)
*   **Data Processing**: ![Pandas](https://img.shields.io/badge/Pandas-2.1.4-150458?logo=pandas&logoColor=white), ![NumPy](https://img.shields.io/badge/NumPy-1.26.4-013243?logo=numpy&logoColor=white) 
*   **Machine Learning**: ![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?logo=scikit-learn&logoColor=white) (train-test split, scaling, KNN, Random Forest), XGBoost
*   **Optimization**: ![SciPy](https://img.shields.io/badge/SciPy-1.11-8CAAE6?logo=scipy&logoColor=white)
 (minimize for portfolio weights)
*   **Visualization**: ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8.4-11557C?logo=matplotlib&logoColor=white)
*   **Other**: Darkdetect for theme detection, datetime for time-series handling
*   **Environment**: ![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) No external databases required (stateful via Streamlit sessions)

This stack emphasizes efficiency, scalability, and integration of data science workflows into production-ready apps.

Installation
------------

1.  **Clone the Repository**:
    
    text
    
        git clone https://github.com/yourusername/tradmincer.git
        cd tradmincer
    
2.  **Set Up Virtual Environment** (Recommended):
    
    text
    
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
    
3.  **Install Dependencies**:
    
    text
    
        pip install -r requirements.txt
    
    _(requirements.txt includes: streamlit, yfinance, pandas, requests, matplotlib, scikit-learn, xgboost, scipy, plotly, feedparser, darkdetect)_
4.  **Run the App**:
    
    text
    
        streamlit run dashboard.py  # Or any entry point like insight.py
    
    Access at http://localhost:8501.

Usage
-----

1.  **Launch the App**: Run as above; navigate via sidebar pages (Insights, Models, News, Portfolio, Ticker, Dashboard).
2.  **Select Stock**: Choose from S&P 500 list; data auto-fetches.
3.  **Interact**:
    *   In **Models**: Train ML models and predict future returns via sidebar inputs.
    *   In **Portfolio**: Add stocks/quantities; optimize and view metrics.
    *   In **Dashboard**: Monitor live prices with auto-refresh every 30 seconds.
4.  **Customization**: Edit date ranges, intervals, or add features via modular code structure.

Example Screenshot:

Failed to load image

[View link](https://via.placeholder.com/800x400?text=Live+Dashboard+Screenshot)

_(Add actual screenshots of key pages for better impact)_

What I Learned & Challenges Overcome
------------------------------------

*   **ML Integration**: Seamlessly embedded training/prediction pipelines into a web app, handling stateful sessions for persistent models.
*   **Optimization Techniques**: Implemented constrained optimization for portfolio weights, balancing return/volatility trade-offs.
*   **Real-time Features**: Managed API rate limits and data freshness with caching and timed refreshes.
*   **UI/UX Best Practices**: Adapted to user themes (dark/light) and used wide layouts for data-dense views.
*   **Edge Cases**: Handled empty data, duplicates, and errors gracefully (e.g., warnings for insufficient data points).
*   **Scalability Insights**: Designed for potential cloud deployment (e.g., Streamlit Sharing or AWS), with no heavy dependencies.

This project honed my ability to deliver end-to-end solutions under constraints, a key skill for big tech environments.

Contributing
------------

Contributions are welcome! Fork the repo, create a branch, and submit a pull request. Focus on:

*   Bug fixes
*   New features (e.g., additional ML models or integrations like Alpha Vantage)
*   Code optimizations

Please follow PEP8 style and include tests where possible.

License
-------

This project is licensed under the MIT License. See LICENSE for details.

Contact
-------

*   **Developer**: Your Name (e.g., John Doe)
*   **Email**: [your.email@example.com](mailto:your.email@example.com)
*   **LinkedIn**: linkedin.com/in/yourprofile
*   **GitHub**: github.com/yourusername
*   **Portfolio**: yourportfolio.com

I'm open to collaborations or discussions on fintech/data projects. Let's connect if you're hiring for roles involving Python, ML, or data apps! 🚀
