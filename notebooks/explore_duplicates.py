import gzip
import json
import pandas as pd

REVIEWS = "data/raw/All_Beauty.jsonl.gz"
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 60)


def read_jsonl(path, fields):
    rows = []
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            rows.append({k: d.get(k) for k in fields})
    return pd.DataFrame(rows)


reviews = read_jsonl(REVIEWS, ["rating", "text", "asin", "parent_asin",
                               "user_id", "timestamp"])
text = reviews["text"].fillna("").str.strip()
lens = text.str.len()

print("=== 1. How many short texts? ===")
for n in [0, 5, 10, 20]:
    print(f"length <= {n}: {(lens <= n).sum()}")

print("\n=== 2. Most common short texts (1-10 chars) ===")
print(text[(lens > 0) & (lens <= 10)].value_counts().head(10))

print("\n=== 3. Most repeated texts ===")
print(text[lens > 0].value_counts().head(10))

print("\n=== 4. Repeated texts that are 50+ chars ===")
print("count:", text[lens >= 50].duplicated().sum())

print("\n=== 5. Same user + product + time ===")
key = ["user_id", "parent_asin", "timestamp"]
print("same key + same asin + same text:",
      reviews.duplicated(key + ["asin", "text"]).sum())
dup = reviews[reviews.duplicated(key, keep=False)].sort_values(key)
print("rows involved:", len(dup))
sample = dup.head(6)[["asin", "parent_asin", "timestamp", "rating"]]
print(sample.assign(text=dup.head(6)["text"].str[:50]))