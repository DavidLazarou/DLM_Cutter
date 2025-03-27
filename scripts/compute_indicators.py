import os
import pandas as pd
import numpy as np
import psycopg2
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

# Load stock prices from database
query = "SELECT ticker, date, adj_close FROM stock_prices ORDER BY ticker, date;"
df = pd.read_sql(query, conn)

# Function to compute indicators for one ticker
def compute_indicators_for_ticker(df_ticker):
    df_ticker = df_ticker.sort_values("date").copy()
    df_ticker.set_index("date", inplace=True)

    results = []

    # Volatility (annualized)
    for window in [10, 20, 30, 50, 60, 90]:
        vol = df_ticker["adj_close"].pct_change().rolling(window).std() * np.sqrt(252)
        results.append(vol.rename(f"vol_{window}d"))

    # Moving Averages
    results.append(df_ticker["adj_close"].rolling(50).mean().rename("sma_50"))
    results.append(df_ticker["adj_close"].rolling(200).mean().rename("sma_200"))
    results.append(df_ticker["adj_close"].ewm(span=50).mean().rename("ema_50"))
    results.append(df_ticker["adj_close"].ewm(span=200).mean().rename("ema_200"))

    # MACD
    ema_12 = df_ticker["adj_close"].ewm(span=12).mean()
    ema_26 = df_ticker["adj_close"].ewm(span=26).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9).mean()
    histogram = macd - signal

    results.append(macd.rename("macd"))
    results.append(signal.rename("macd_signal"))
    results.append(histogram.rename("macd_hist"))

    df_ind = pd.concat(results, axis=1).reset_index()
    df_ind["ticker"] = df_ticker["ticker"].iloc[0]

    return df_ind

# Group by ticker and compute all
all_indicators = (
    df.groupby("ticker")
    .apply(compute_indicators_for_ticker)
    .reset_index(drop=True)
)

# Reshape into long format
long_df = all_indicators.melt(
    id_vars=["ticker", "date"],
    var_name="indicator_name",
    value_name="value"
).dropna()

# Insert into stock_indicators table
insert_query = """
INSERT INTO stock_indicators (ticker, date, indicator_name, value)
VALUES (%s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

for row in long_df.itertuples(index=False):
    cur.execute(insert_query, (row.ticker, row.date, row.indicator_name, row.value))

conn.commit()
cur.close()
conn.close()

print("✅ Indicators computed and inserted.")
