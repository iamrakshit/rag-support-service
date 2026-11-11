"""Loads the low-code policy file (policies/access_policies.json) and applies it."""
import json
import re

from . import config

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"\b\d{3}[-. ]\d{3}[-. ]\d{4}\b")
CARD = re.compile(r"\b(?:\d[ -]?){12,19}\b")


class PolicyEngine:
    def __init__(self, path=config.POLICY_PATH):
        self.policy = json.loads(path.read_text(encoding="utf-8"))
        self.injection = [re.compile(p, re.I) for p in self.policy["block_injection"]["patterns"]]
        self.handoff = [re.compile(p, re.I) for p in self.policy["handoff_intents"]["patterns"]]
        self.gate = self.policy["confidence_gate"]

    def is_injection(self, message):
        return any(p.search(message) for p in self.injection)

    def needs_human(self, message):
        return any(p.search(message) for p in self.handoff)

    def redact(self, text):
        rules = set(self.policy["redact_in_replies"])
        if "email" in rules:
            text = EMAIL.sub("[email redacted]", text)
        if "phone" in rules:
            text = PHONE.sub("[phone redacted]", text)
        if "card_number" in rules:
            text = CARD.sub("[card redacted]", text)
        return text
