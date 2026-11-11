"""ETL: help-centre export -> clean articles + embeddings -> MongoDB (or a local index file).

Extract   read data/raw/help_center_export.csv
Transform drop drafts/archived/duplicate rows, strip HTML and whitespace, fit TF-IDF, embed each article
Load      upsert into MongoDB collections `articles` and `meta`, or write data/processed/index.json

Usage:  python -m etl.load_kb                 # local index (default)
        STORE_BACKEND=mongo python -m etl.load_kb
"""
import csv
import html
import json
import re

from app import config
from app.embeddings import TfidfEmbedder

RAW = config.ROOT / "data" / "raw" / "help_center_export.csv"


def extract(path=RAW):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clean_html(text):
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def transform(rows):
    report = {"rows_in": len(rows), "dropped_unpublished": 0, "dropped_missing_id": 0, "dropped_duplicates": 0}
    seen, articles = set(), []
    for r in sorted(rows, key=lambda r: r.get("last_updated", ""), reverse=True):  # newest version wins
        if not r.get("article_id"):
            report["dropped_missing_id"] += 1
            continue
        if r.get("status") != "published":
            report["dropped_unpublished"] += 1
            continue
        if r["article_id"] in seen:
            report["dropped_duplicates"] += 1
            continue
        seen.add(r["article_id"])
        articles.append({"id": r["article_id"], "category": r["category"].strip(), "title": r["title"].strip(),
                         "body": clean_html(r["body_html"]), "last_updated": r["last_updated"]})
    articles.sort(key=lambda a: a["id"])
    embedder = TfidfEmbedder().fit([a["title"] + " " + a["body"] for a in articles])
    for a in articles:
        a["embedding"] = embedder.embed(a["title"] + " " + a["body"])
    report["articles_out"] = len(articles)
    return articles, embedder, report


def load(articles, embedder):
    if config.STORE_BACKEND == "mongo":
        from pymongo import MongoClient, ReplaceOne

        db = MongoClient(config.MONGO_URI)[config.MONGO_DB]
        db["articles"].bulk_write([ReplaceOne({"id": a["id"]}, a, upsert=True) for a in articles])
        db["articles"].create_index("id", unique=True)
        db["meta"].replace_one({"_id": "embedder"}, {"_id": "embedder", "value": embedder.to_dict()}, upsert=True)
        return f"MongoDB {config.MONGO_URI}/{config.MONGO_DB}"
    config.INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.INDEX_PATH.write_text(json.dumps({"embedder": embedder.to_dict(), "documents": articles}), encoding="utf-8")
    return str(config.INDEX_PATH.relative_to(config.ROOT))


def run():
    articles, embedder, report = transform(extract())
    target = load(articles, embedder)
    print(f"ETL complete -> {target}")
    for k, v in report.items():
        print(f"  {k}: {v}")
    return report


if __name__ == "__main__":
    run()
