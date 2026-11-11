"""Vector store with two interchangeable backends.

MemoryVectorStore: reads the index produced by the ETL from data/processed/index.json.
MongoVectorStore:  reads articles and embeddings from MongoDB collections written by the ETL.
Both expose the same search() method, so the assistant never knows which one it is using.
"""
import json

from . import config
from .embeddings import TfidfEmbedder, cosine


class MemoryVectorStore:
    def __init__(self, index=None, path=config.INDEX_PATH):
        index = index or json.loads(path.read_text(encoding="utf-8"))
        self.embedder = TfidfEmbedder.from_dict(index["embedder"])
        self.docs = index["documents"]

    def search(self, query, k=3, expand=False):
        q = self.embedder.embed(query, expand=expand)
        scored = [(cosine(q, d["embedding"]), d) for d in self.docs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:k]


class MongoVectorStore(MemoryVectorStore):
    def __init__(self, uri=config.MONGO_URI, db=config.MONGO_DB):
        from pymongo import MongoClient  # imported only when MongoDB is used

        database = MongoClient(uri)[db]
        meta = database["meta"].find_one({"_id": "embedder"})
        docs = list(database["articles"].find({}, {"_id": 0}))
        super().__init__(index={"embedder": meta["value"], "documents": docs})


def get_store():
    return MongoVectorStore() if config.STORE_BACKEND == "mongo" else MemoryVectorStore()
