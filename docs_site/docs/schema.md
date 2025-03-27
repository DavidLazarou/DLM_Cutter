# Database Schema

## fred_series

| Column Name   | Type        | Description                            |
|---------------|-------------|----------------------------------------|
| id            | SERIAL      | Primary key                            |
| series_id     | TEXT        | FRED series code (e.g., `INDPRO`)      |
| observation_date | DATE     | Date of the observation                |
| value         | NUMERIC     | Value reported by FRED                 |
| retrieved_at  | TIMESTAMP   | When data was inserted into Postgres  |

### Table Snapshot
```sql
CREATE TABLE fred_series (
  id SERIAL PRIMARY KEY,
  series_id TEXT NOT NULL,
  observation_date DATE NOT NULL,
  value NUMERIC,
  retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
