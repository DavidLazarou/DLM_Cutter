import requests
import psycopg2
from datetime import datetime

# --- Config ---
CIK = "0000018230"
TICKER = "CAT"
METRIC = "RevenueFromContractWithCustomerExcludingAssessedTax"  # <-- Try this first
STATEMENT_TYPE = "income"
USER_AGENT = "dlm_research/1.0 (dave@dlmfund.dev)"

URL = f"https://data.sec.gov/api/xbrl/companyconcept/{CIK}/us-gaap/{METRIC}.json"

# --- DB Connection ---
conn = psycopg2.connect(
    dbname="dlm_research",
    user="dave",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# --- HTTP GET ---
headers = {
    "User-Agent": USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov",
    "Connection": "keep-alive"
}

resp = requests.get(URL, headers=headers)

# --- Debug the response ---
print(f"HTTP Status Code: {resp.status_code}")
print("Response preview:", resp.text[:300])

try:
    data = resp.json()
except requests.exceptions.JSONDecodeError:
    print("❌ JSON decode failed — likely issue with User-Agent or invalid concept.")
    exit(1)

# --- Insert Entries ---
entries = data.get("units", {}).get("USD", [])
print(f"📦 Found {len(entries)} entries in response.")

for entry in entries:
    fiscal_date = entry.get("end")
    value = entry.get("val")
    form = entry.get("form", "SEC")

    cur.execute("""
        INSERT INTO company_fundamentals (
            cik, ticker, fiscal_date, statement_type,
            metric, value, unit, source
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (
        CIK, TICKER, fiscal_date, STATEMENT_TYPE,
        METRIC, value, "USD", form
    ))

# --- Commit & Close ---
conn.commit()
cur.close()
conn.close()

print(f"✅ Inserted {len(entries)} revenue entries for CAT.")
