"""Mock order lookup tool. The improved assistant enforces ownership and verification."""
import json
import re
from pathlib import Path

CUSTOMERS_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"
ORDER_ID = re.compile(r"\b(10\d{2})\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def load_customers(path: Path = CUSTOMERS_PATH) -> list:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def find_mentions(message: str, customers: list) -> list:
    ids = set(ORDER_ID.findall(message))
    emails = {e.lower() for e in EMAIL.findall(message)}
    return [c for c in customers if c["order_id"] in ids or c["email"] in emails]


def full_record(c: dict) -> str:
    return (f"Order {c['order_id']} for {c['name']} ({c['email']}, {c['phone']}), "
            f"shipping to {c['address']}, paid with card ending {c['card_last4']}. Status: {c['status']}.")


def status_only(c: dict) -> str:
    return f"Order {c['order_id']} for {c['name']} is currently: {c['status']}."
