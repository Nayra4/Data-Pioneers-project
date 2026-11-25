"""Mock REST API that serves part of the reviews."""
import json
from pathlib import Path

from fastapi import FastAPI, Query

DATA = Path(__file__).resolve().parent.parent / "data" / "sources" / "api_reviews.json"
app = FastAPI(title="Mock Reviews API")


@app.get("/reviews")
def get_reviews(offset: int = Query(0, ge=0), limit: int = Query(500, ge=1, le=1000)):
    rows = json.loads(DATA.read_text(encoding="utf-8"))
    return {"total": len(rows), "data": rows[offset:offset + limit]}
