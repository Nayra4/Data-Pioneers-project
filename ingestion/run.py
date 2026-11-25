"""Single entry point for Airflow: ingest all sources into raw_reviews."""
import logging

from ingestion.load_raw import load_raw, unify_sources

log = logging.getLogger(__name__)


def run_ingestion():
    """Read CSV + API + DB, unify them and load raw_reviews."""
    df = unify_sources()
    log.info("rows by source: %s", df["source"].value_counts().to_dict())
    rows = load_raw(df)
    log.info("loaded %s rows into raw_reviews", rows)
    return rows


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("rows loaded:", run_ingestion())