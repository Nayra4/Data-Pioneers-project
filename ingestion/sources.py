"""Read reviews from the CSV file and the REST API."""
import os

import pandas as pd
import requests

CSV_PATH = os.getenv("CSV_PATH", "data/sources/csv_reviews.csv")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/reviews")
COLUMNS = ["review_id", "product_id", "category", "review_text", "rating", "review_date"]


def read_csv_source(path=CSV_PATH):
    df = pd.read_csv(path, dtype={"review_id": str, "product_id": str})
    return df[COLUMNS].assign(source="csv")


def read_api_source(url=API_URL, page_size=500):
    rows, offset = [], 0
    while True:
        response = requests.get(url, params={"offset": offset, "limit": page_size}, timeout=30)
        response.raise_for_status()
        page = response.json()["data"]
        if not page:
            break
        rows.extend(page)
        offset += page_size
    return pd.DataFrame(rows, columns=COLUMNS).assign(source="api")


if __name__ == "__main__":
    print("csv:", read_csv_source().shape)
    print("api:", read_api_source().shape)