import gzip
import json
import pandas as pd

REVIEWS = "data/raw/All_Beauty.jsonl.gz"
META = "data/raw/meta_All_Beauty.jsonl.gz"


def read_jsonl(path, fields):
    """Read a .jsonl.gz file line by line, keeping only the given fields."""
    rows = []
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            rows.append({k: d.get(k) for k in fields})
    return pd.DataFrame(rows)


reviews = read_jsonl(REVIEWS, ["rating", "title", "text", "parent_asin",
                               "user_id", "timestamp", "helpful_vote",
                               "verified_purchase"])
meta = read_jsonl(META, ["parent_asin", "title", "main_category"])

print("=== 1. Shape ===")
print("reviews:", reviews.shape, "| meta:", meta.shape)

print("\n=== 2. Nulls per column (reviews) ===")
print(reviews.isna().sum())

print("\n=== 3. Empty text ===")
print("empty text:", (reviews["text"].fillna("").str.strip() == "").sum())

print("\n=== 4. Rating distribution ===")
print(reviews["rating"].value_counts().sort_index())

print("\n=== 5. Dates ===")
dates = pd.to_datetime(reviews["timestamp"], unit="ms")
print("min:", dates.min(), "| max:", dates.max())
print(dates.dt.year.value_counts().sort_index())

print("\n=== 6. Text length (characters) ===")
print(reviews["text"].fillna("").str.len().describe())

print("\n=== 7. Duplicates ===")
print("same user+product+time:",
      reviews.duplicated(["user_id", "parent_asin", "timestamp"]).sum())
print("same text:", reviews["text"].duplicated().sum())

print("\n=== 8. Link reviews to metadata ===")
matched = reviews["parent_asin"].isin(meta["parent_asin"]).mean()
print(f"reviews that have a product in meta: {matched:.1%}")
print(meta["main_category"].value_counts(dropna=False).head(5))