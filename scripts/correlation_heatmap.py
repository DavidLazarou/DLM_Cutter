import os
import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD,
    dbname=PG_DATABASE
)

# Query the last 90 days of stock prices
query = """
    SELECT ticker, date, adj_close
    FROM stock_prices
    WHERE date >= CURRENT_DATE - INTERVAL '90 days'
"""
df = pd.read_sql(query, conn)
conn.close()

# Pivot to wide format
df_wide = df.pivot(index="date", columns="ticker", values="adj_close")

# Compute daily returns
returns = df_wide.pct_change().dropna()

# Compute correlation matrix
correlation_matrix = returns.corr()

# Plot heatmap
plt.figure(figsize=(16, 12))  # Larger figure
sns.set(font_scale=0.8)       # Smaller font
sns.heatmap(
    correlation_matrix,
    cmap="coolwarm",
    square=True,
    linewidths=0.5,
    linecolor="lightgray",
    cbar=True,
    xticklabels=True,
    yticklabels=True,
    annot=False  # Turn off annotations for readability
)

plt.title("90-Day Correlation Matrix of Daily Returns", fontsize=16)
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
