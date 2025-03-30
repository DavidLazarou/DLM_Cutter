import pandas as pd
import os
import re
import numpy as np
import yaml
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# --- Load Config ---
CONFIG_PATH = "../config/config.yaml"
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

ingest_cfg = config["ingest"]
db_cfg = config["database"]

DATA_DIR = ingest_cfg["data_dir"]
FILENAME = ingest_cfg["file_name"]
LOG_DIR = ingest_cfg["logs_dir"]
TABLE_NAME = ingest_cfg["table_name"]
CRITICAL_COLUMNS = set(ingest_cfg["critical_columns"])
TO_NUMERIC = set(ingest_cfg.get("columns_to_numeric", []))  # Optional

FILEPATH = os.path.join(DATA_DIR, FILENAME)
os.makedirs(LOG_DIR, exist_ok=True)

# --- PostgreSQL connection ---
DATABASE_URL = f"postgresql://{db_cfg['user']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['dbname']}"
engine = create_engine(DATABASE_URL)

# --- Column Cleaning Helpers ---
def clean_column_name(col):
    col = col.lower().replace('%', 'pct')
    col = re.sub(r'[^a-zA-Z0-9]', '_', col)
    col = re.sub(r'_+', '_', col).strip('_')
    return col

def deduplicate_columns(cols):
    seen = {}
    new_cols = []
    for col in cols:
        if col not in seen:
            seen[col] = 1
            new_cols.append(col)
        else:
            new_name = f"{col}_{seen[col]}"
            seen[col] += 1
            new_cols.append(new_name)
    return new_cols

# --- Load CSV ---
df = pd.read_csv(FILEPATH)
print(f"\n✅ Loaded CSV: {FILEPATH} with shape {df.shape}")

df.columns = deduplicate_columns([clean_column_name(c) for c in df.columns])
df.columns = [f"c_{col}" if re.match(r'^\d', col) else col for col in df.columns]

# Fix mismatches
df = df.rename(columns={
    "last_yr_s_eps_f0_before_nri": "last_yrs_eps_f0_before_nri",
    "f_1_consensus_sales_est_mil": "f1_consensus_sales_est_mil",
    "q_1_consensus_sales_est_mil": "q1_consensus_sales_est_mil"
})

# --- Report Date ---
report_date = datetime.strptime(FILENAME.split("_")[-1].replace(".csv", ""), "%Y-%m-%d").date()
df["report_date"] = report_date
print(f"\n📅 Set report_date = {report_date}")

# --- Save Schema Snapshot ---
schema_log_path = os.path.join(LOG_DIR, f"zacks_column_schema_{report_date}.csv")
pd.DataFrame({"column_name": df.columns}).to_csv(schema_log_path, index=False)
print(f"\n📄 Saved schema snapshot to: {schema_log_path}")

# --- Check Schema Drift ---
previous_date = report_date - timedelta(days=1)
previous_log_path = os.path.join(LOG_DIR, f"zacks_column_schema_{previous_date}.csv")
removed = []
removed_critical = []

if os.path.exists(previous_log_path):
    prev_cols = pd.read_csv(previous_log_path)["column_name"].tolist()
    removed = [col for col in prev_cols if col not in df.columns]
    removed_critical = [col for col in removed if col in CRITICAL_COLUMNS]
    print(f"\n❌ Columns removed since yesterday:")
    for col in removed:
        print(f"  - {col}")
else:
    print(f"\n📂 No previous schema file found — skipping drift check.")

# --- Save HTML Drift Report ---
html_report_path = os.path.join(LOG_DIR, f"zacks_report_{report_date}.html")
with open(html_report_path, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Zacks Ingestion Report — {report_date}</title>
</head>
<body>
  <h1>Zacks Ingestion Report — {report_date}</h1>
  <p><strong>CSV Loaded:</strong> {FILENAME} with shape {df.shape}</p>
  <p><strong>Report Date:</strong> {report_date}</p>
  <p><strong>Schema Snapshot:</strong> {schema_log_path}</p>
  <h2>Schema Drift</h2>
  <ul>
    {''.join(f'<li>{"🚨" if col in removed_critical else "⚠️"} {col}</li>' for col in removed)}
  </ul>
</body>
</html>
""")
print(f"\n📊 Saved HTML report to: {html_report_path}")

# --- Stop on Critical Drift ---
if removed_critical:
    raise Exception(f"🛑 Ingestion halted: critical columns removed → {removed_critical}")

# --- Convert Numeric Columns ---
for col in TO_NUMERIC:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --- Derived Metrics ---
df["eg1"] = (df["f1_consensus_est"] - df["last_yrs_eps_f0_before_nri"]) / df["last_yrs_eps_f0_before_nri"]
df["eg2"] = (df["f2_consensus_est"] - df["f1_consensus_est"]) / df["f1_consensus_est"]
df["pe1"] = df["last_close"] / df["f1_consensus_est"]
df["pe2"] = df["last_close"] / df["f2_consensus_est"]
df["ps1"] = df["last_close"] / (df["f1_consensus_sales_est_mil"] / df["shares_outstanding_mil"])
df["ps2"] = df["last_close"] / (df["q1_consensus_sales_est_mil"] / df["shares_outstanding_mil"])
df["peg1"] = df["pe1"] / df["eg1"]
df["peg2"] = df["pe2"] / df["eg2"]
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# --- Remove Duplicates for Day ---
with engine.connect() as conn:
    existing = pd.read_sql(
        f"SELECT ticker FROM {TABLE_NAME} WHERE report_date = %(report_date)s",
        con=conn.connection,
        params={"report_date": report_date}
    )
    existing_tickers = set(existing["ticker"].dropna().unique().tolist())

original_count = len(df)
df = df[~df["ticker"].isin(existing_tickers)]
print(f"\n🧹 Removed {original_count - len(df)} duplicates. {len(df)} rows left to insert.")

# --- Preview Metrics ---
print("\n🔍 Preview of calculated fields:")
print(df[["ticker", "eg1", "pe1", "peg1", "report_date"]].head())

# --- Insert & Audit Log ---
if len(df) > 0:
    try:
        print(f"\n🚀 Inserting {len(df)} rows into '{TABLE_NAME}'...")
        df.to_sql(TABLE_NAME, engine, if_exists="append", index=False)
        print(f"✅ Inserted {len(df)} rows into '{TABLE_NAME}' successfully.")

        audit_row = {
            "report_date": report_date,
            "file_name": FILENAME,
            "rows_inserted": len(df),
            "rows_skipped": original_count - len(df),
        }

        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO zacks_ingest_log (report_date, file_name, rows_inserted, rows_skipped)
                    VALUES (:report_date, :file_name, :rows_inserted, :rows_skipped)
                    ON CONFLICT (report_date) DO UPDATE
                    SET file_name = EXCLUDED.file_name,
                        rows_inserted = EXCLUDED.rows_inserted,
                        rows_skipped = EXCLUDED.rows_skipped;
                """),
                audit_row
            )
        print(f"🗒️ Logged ingestion to 'zacks_ingest_log': {audit_row}")

    except Exception as e:
        print(f"\n❌ Failed to insert: {e}")
else:
    print("📭 No new rows to insert.")
