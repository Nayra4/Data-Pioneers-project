# AI-Enhanced Customer Feedback Data Pipeline

An ETL pipeline that ingests Amazon product reviews from several sources
(CSV, REST API, PostgreSQL), cleans and validates the text, enriches every
review with a Hugging Face sentiment model, stores the results in PostgreSQL,
and orchestrates everything with Apache Airflow.

Data: [Amazon Reviews 2023](https://amazon-reviews-2023.github.io) (McAuley Lab).

## Project structure

| Folder | Purpose |
|---|---|
| `ingestion/` | Read reviews from CSV, API and PostgreSQL |
| `processing/` | Text cleaning, validation and de-duplication |
| `quality/` | Data-quality checks |
| `mock_api/` | FastAPI service that acts as the API source |
| `ai/` | Sentiment model, tokenization, batch inference |
| `notebooks/` | Model comparison |
| `sql/` | Database schema |
| `dags/` | Airflow DAG |
| `dashboard/`, `analytics/` | Aggregations and dashboard |
| `docs/` | Architecture diagram and documentation |
| `tests/` | Unit tests |

> Setup, usage and results sections will be added as the project progresses.