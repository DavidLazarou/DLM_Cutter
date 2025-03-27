import os
import pandas as pd
import numpy as np
import psycopg2
from itertools import combinations
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

# Connect to database
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD,
    dbname=PG_DATABASE
)
cur = conn.cursor()

# Load stock prices into wide format
query = "SELECT date, ticker, adj_close FROM stock_prices ORDER BY date;"
df = pd.read_sql(query, conn)
price_df = df.pivot(index="date", columns="ticker", values="adj_close").sort_index()
returns = price_df.pct_change().dropna()

# Define rolling windows
windows = [30, 60, 90]

# Generate all unique ticker pairs
tickers = returns.columns
ticker_pairs = list(combinations(tickers, 2))

# Prepare rows for insertion
records = []

for window in windows:
    rolling_corr = returns.rolling(window).corr()

    for date in rolling_corr.index.get_level_values(0).unique():
        for ticker1, ticker2 in ticker_pairs:
            try:
                corr_value = rolling_corr.loc[date].loc[ticker1, ticker2]
                if pd.notnull(corr_value):
                    # ✅ Convert correlation to native float
                    records.append((date, ticker1, ticker2, window, float(corr_value)))
            except KeyError:
                continue  # skip if data is missing

# Insert into database
insert_query = """
INSERT INTO rolling_correlations (date, ticker1, ticker2, window_size, correlation)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

cur.executemany(insert_query, records)

conn.commit()
cur.close()
conn.close()

print("✅ Rolling correlations computed and inserted.")
