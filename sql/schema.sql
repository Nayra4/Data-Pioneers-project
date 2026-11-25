-- raw data is kept as is (duplicates allowed, so no primary key)
CREATE TABLE IF NOT EXISTS raw_reviews (
    review_id TEXT, source TEXT, product_id TEXT, category TEXT,
    review_text TEXT, rating NUMERIC, review_date TIMESTAMP, ingested_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clean_reviews (
    review_id TEXT PRIMARY KEY, product_id TEXT, category TEXT,
    clean_text TEXT, review_date TIMESTAMP, is_valid BOOLEAN
);

CREATE TABLE IF NOT EXISTS enriched_reviews (
    review_id TEXT PRIMARY KEY, sentiment TEXT, confidence NUMERIC,
    model_name TEXT, processed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS failed_inference (
    review_id TEXT, error_message TEXT, attempts INTEGER, failed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sentiment_summary (
    product_id TEXT, category TEXT, date DATE, sentiment TEXT,
    review_count INTEGER, avg_confidence NUMERIC
);