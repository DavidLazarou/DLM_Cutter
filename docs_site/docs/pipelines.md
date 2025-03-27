# Data Pipelines

## FRED → PostgreSQL

### Purpose
Pull key economic time series (e.g. Industrial Production, Core PCE) from the FRED API and store in PostgreSQL for analysis and modeling.

### Data Sources
- [FRED](https://fred.stlouisfed.org/)
- Series IDs:
  - `INDPRO`: Industrial Production
  - `DGORDER`: Durable Goods Orders
  - `PCEPILFE`: Core PCE Price Index
  - `PI`: US Personal Income
  - `PCE`: US Personal Spending

### Workflow
1. `fetch_fred_data.py`
   - Loads FRED API key from `.env`
   - Pulls selected series as Pandas DataFrame
2. `store_fred_to_postgres.py`
   - Connects to Postgres using credentials from `.env`
   - Transforms and inserts records into `fred_series` table

### Automation
- Cron job (planned): `@daily` schedule to re-run scripts
- Future: Move to Airflow or Dagster pipeline

### Tests / Validation
- Row counts per series
- Timestamp verification
- Duplication handling

### Sample Output
```sql
SELECT COUNT(*) FROM fred_series WHERE series_id = 'INDPRO';
