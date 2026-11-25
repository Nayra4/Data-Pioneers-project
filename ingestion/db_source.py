"""Load the DB-source sample into PostgreSQL and read it back."""
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_CSV_PATH = os.getenv("DB_CSV_PATH", "data/sources/db_reviews.csv")
SOURCE_TABLE = "src_db_reviews"
COLUMNS = ["review_id", "product_id", "category", "review_text", "rating", "review_date"]


def get_engine():
    return create_engine(os.environ["DB_URL"])


def load_db_source(csv_path=DB_CSV_PATH):
    """One-time setup: copy db_reviews.csv into a PostgreSQL table."""
    df = pd.read_csv(csv_path, dtype={"review_id": str, "product_id": str})
    df["review_date"] = pd.to_datetime(df["review_date"])
    df[COLUMNS].to_sql(SOURCE_TABLE, get_engine(), if_exists="replace", index=False)
    return len(df)


def read_db_source():
    """Ingestion function for source #3: read the table with SQL."""
    query = f"SELECT {', '.join(COLUMNS)} FROM {SOURCE_TABLE}"
    df = pd.read_sql(query, get_engine())
    return df.assign(source="db")


if __name__ == "__main__":
    print("loaded rows:", load_db_source())
    print("db:", read_db_source().shape)