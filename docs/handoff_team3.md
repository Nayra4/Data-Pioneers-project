# Ingestion: how to run it

## Setup
1. `pip install -r requirements.txt`
2. Create `.env` in the project root:
   `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DB_URL`
3. Start PostgreSQL:
   `docker run -d --name feedback-db --env-file .env -p 5433:5432 -v feedback-pgdata:/var/lib/postgresql/data postgres:16`
4. Create the tables using `sql/schema.sql`.

## Prepare the data (once)
```powershell
mkdir data\raw
curl.exe -L -o data\raw\All_Beauty.jsonl.gz "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/All_Beauty.jsonl.gz"
curl.exe -L -o data\raw\meta_All_Beauty.jsonl.gz "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_All_Beauty.jsonl.gz"
python ingestion/prepare_sources.py
python -m ingestion.db_source
```

## Run
1. Start the API: `uvicorn mock_api.main:app --port 8000`
2. Run: `python -m ingestion.run` (expected: 10200 rows)

## For Airflow
- Call `run_ingestion()` from `ingestion.run`.
- The mock API must run as a service in docker-compose.
- Set `DB_URL`, `API_URL`, `CSV_PATH`, `DB_CSV_PATH` to match the containers.
- Not tested inside Airflow yet.
- `src_db_reviews` is the database source table, not part of the shared contract.