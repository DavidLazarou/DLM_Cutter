from datetime import date
from sqlalchemy import create_engine, text

# --- DB connection ---
DB_USER = "dave"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "dlm_research"
DATABASE_URL = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Test Audit Log Entry ---
test_log = {
    "report_date": date(2025, 3, 30),  # Use a test date
    "file_name": "zacks_custom_screen_2025-03-30_test.csv",
    "rows_inserted": 999,
    "rows_skipped": 42
}

# --- Insert into Audit Log ---
engine = create_engine(DATABASE_URL)

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
        test_log
    )

print("✅ Test audit log inserted successfully.")
