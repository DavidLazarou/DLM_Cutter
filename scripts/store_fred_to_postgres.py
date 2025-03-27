import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from fredapi import Fred

# Load environment variables
load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

# Connect to FRED
fred = Fred(api_key=FRED_API_KEY)

# List of FRED series you want to track
fred_series = {
    "INDPRO": "Industrial Production Index",
    "DGORDER": "Durable Goods Orders",
    "PCEPILFE": "Core PCE Price Index",
    "PI": "US Personal Income",
    "PCE": "US Personal Spending"
}

# Build PostgreSQL connection parameters
conn_params = {
    "host": PG_HOST,
    "port": PG_PORT,
    "user": PG_USER,
    "dbname": PG_DATABASE
}

# Only include password if it's available (for CI/CD or password-based systems)
if PG_PASSWORD:
    conn_params["password"] = PG_PASSWORD

# Connect to Postgres
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

# Insert data
for series_id, description in fred_series.items():
    data = fred.get_series(series_id)
    df = data.reset_index()
    df.columns = ["observation_date", "value"]

    print(f"Inserting {len(df)} rows for {series_id} ({description})...")

    for row in df.itertuples(index=False):
        cur.execute("""
            INSERT INTO fred_series (series_id, observation_date, value)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (series_id, row.observation_date, row.value))

# Commit and close
conn.commit()
cur.close()
conn.close()

print("✅ All data inserted.")
