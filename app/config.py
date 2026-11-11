"""Configuration from environment variables.

STORE_BACKEND = "memory" (default, no database needed) or "mongo"
MONGO_URI     = mongodb://localhost:27017
MONGO_DB      = support_rag
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE_BACKEND = os.getenv("STORE_BACKEND", "memory")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "support_rag")
INDEX_PATH = ROOT / "data" / "processed" / "index.json"
POLICY_PATH = ROOT / "policies" / "access_policies.json"
