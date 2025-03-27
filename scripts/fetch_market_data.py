import yfinance as yf
import pandas as pd
import psycopg2
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Database connection parameters
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

# Define tickers (33 tickers across 11 sectors, 3 per sector)
tickers = [
    "AAPL", "MSFT", "NVDA",    # Tech
    "JPM", "BAC", "WFC",       # Financials
    "XOM", "CVX", "COP",       # Energy
    "META", "GOOG", "NFLX",    # Communications
    "GE", "RTX", "CAT",        # Industrials
    "LLY", "JNJ", "UNH",       # Healthcare
    "LIN", "SHW", "ECL",       # Basic Materials
    "AMZN", "TSLA", "HD",      # Consumer Discretionary
    "COST", "PG", "WMT",       # Consumer Staples
    "NEE", "SO", "DUK",        # Utilities
    "PLD", "AMT", "WELL"       # Real Estate (Fixed WELL typo)
]

# Date range
end_date = datetime.today()
start_date = end_date - timedelta(days=365 * 5)  # 5 years

# Fetch adjusted close prices (auto_adjust=True)
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)["Close"]
data = data.dropna(how="all")
data.columns.name = "ticker"  # for melting
data = data.reset_index().melt(id_vars=["Date"], var_name="ticker", value_name="adj_close")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD,
    dbname=PG_DATABASE
)
cur = conn.cursor()

# Insert into stock_prices table
for row in data.itertuples(index=False):
    cur.execute("""
        INSERT INTO stock_prices (ticker, date, adj_close)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (row.ticker, row.Date, row.adj_close))

conn.commit()
cur.close()
conn.close()

print("✅ Historical stock prices inserted into stock_prices table.")
