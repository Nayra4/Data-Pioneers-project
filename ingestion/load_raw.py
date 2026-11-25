"""Unify the 3 sources and store them in the raw_reviews table."""
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import text

from ingestion.db_source import get_engine, read_db_source
from ingestion.sources import read_api_source, read_csv_source

RAW_COLUMNS = ["review_id", "source", "product_id", "category",
               "review_text", "rating", "review_date", "ingested_at"]

DDL = """
CREATE TABLE IF NOT EXISTS raw_reviews (
    review_id    TEXT,
    source       TEXT,
    product_id   TEXT,
    category     TEXT,
    review_text  TEXT,
    rating       NUMERIC,
    review_date  TIMESTAMP,
    ingested_at  TIMESTAMP
)
"""


def unify_sources():
    """Read the 3 sources and return one DataFrame with the contract columns."""
    frames = [read_csv_source(), read_api_source(), read_db_source()]
    df = pd.concat(frames, ignore_index=True)
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["ingested_at"] = datetime.now(timezone.utc).replace(tzinfo=None)
    return df[RAW_COLUMNS]


def load_raw(df, engine=None):
    """Replace the content of raw_reviews with df (safe to re-run)."""
    engine = engine or get_engine()
    with engine.begin() as conn:
        conn.execute(text(DDL))
        conn.execute(text("TRUNCATE TABLE raw_reviews"))
        df.to_sql("raw_reviews", conn, if_exists="append", index=False)
    return len(df)


if __name__ == "__main__":
    data = unify_sources()
    print("rows by source:")
    print(data["source"].value_counts())
    print("null dates:", data["review_date"].isna().sum())
    print("exact duplicate review_id:", data["review_id"].duplicated().sum())
    print("loaded:", load_raw(data))