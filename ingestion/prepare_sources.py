"""Sample All_Beauty reviews and split them into three sources."""
import gzip
import hashlib
import json
from pathlib import Path

import pandas as pd

REVIEWS = "data/raw/All_Beauty.jsonl.gz"
META = "data/raw/meta_All_Beauty.jsonl.gz"
OUT = Path("data/sources")
SAMPLE_SIZE = 10_000
SEED = 42


def read_jsonl(path, fields):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        rows = [{k: d.get(k) for k in fields} for d in map(json.loads, f)]
    return pd.DataFrame(rows)


def make_review_id(row):
    key = f"{row['user_id']}|{row['parent_asin']}|{row['timestamp']}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


reviews = read_jsonl(REVIEWS, ["rating", "title", "text", "parent_asin",
                               "user_id", "timestamp"])
df = reviews.sample(SAMPLE_SIZE, random_state=SEED).reset_index(drop=True)

meta = read_jsonl(META, ["parent_asin", "main_category"])
df = df.merge(meta.drop_duplicates("parent_asin"), on="parent_asin", how="left")

df["review_id"] = df.apply(make_review_id, axis=1)
df["review_text"] = (df["title"].fillna("") + " " + df["text"].fillna("")).str.strip()
df["review_date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.strftime("%Y-%m-%d %H:%M:%S")
df = df.rename(columns={"parent_asin": "product_id", "main_category": "category"})
df = df[["review_id", "product_id", "category", "review_text", "rating", "review_date"]]

# Inject errors on purpose, to demonstrate cleaning
bad = df.sample(200, random_state=SEED).index
df.loc[bad[:100], "review_text"] = ""
df.loc[bad[100:150], "rating"] = 9.0
df.loc[bad[150:], "review_date"] = "2099-01-01 00:00:00"

# Add 200 duplicates, then shuffle
duplicates = df.sample(200, random_state=SEED + 1)
df = pd.concat([df, duplicates]).sample(frac=1, random_state=SEED).reset_index(drop=True)

OUT.mkdir(parents=True, exist_ok=True)
a, b = int(len(df) * 0.4), int(len(df) * 0.7)
df.iloc[:a].to_csv(OUT / "csv_reviews.csv", index=False)
df.iloc[a:b].to_json(OUT / "api_reviews.json", orient="records", force_ascii=False)
df.iloc[b:].to_csv(OUT / "db_reviews.csv", index=False)

print("total:", len(df), "| csv:", a, "| api:", b - a, "| db:", len(df) - b)
print("duplicate ids:", df["review_id"].duplicated().sum())
print("empty text:", (df["review_text"] == "").sum())