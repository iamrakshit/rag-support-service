"""Baseline and improved RAG assistants over the vector store.

Baseline (sprint 1): vector search on the customer's exact words, always answers, looks up any order mentioned.
Improved (sprints 2-3): vocabulary expansion, confidence gate with human handoff, and the low-code access
policies (injection blocking, sensitive-intent handoff, order ownership checks, PII redaction).
"""
from dataclasses import dataclass, field
from typing import Optional

from . import llm
from .orders import EMAIL, find_mentions, full_record, load_customers, status_only
from .policies import PolicyEngine
from .vector_store import get_store

HANDOFF = ("I want to make sure this is handled properly, so I'm passing your conversation to a member of our "
           "support team. They'll see everything you've shared, so you won't need to repeat it.")
REFUSE = ("I can't help with that request. For your security, I can only share order details with the account "
          "holder. Please sign in, or provide your order number together with the email used at checkout.")


@dataclass
class Reply:
    action: str                     # answer | handoff | refuse
    text: str
    article_id: Optional[str] = None
    score: float = 0.0
    reasons: list = field(default_factory=list)


class BaselineAssistant:
    def __init__(self, store=None, customers=None):
        self.store = store or get_store()
        self.customers = customers or load_customers()

    def respond(self, message, session_email=None):
        mentions = find_mentions(message, self.customers)
        if mentions:
            return Reply("answer", " ".join(full_record(c) for c in mentions), reasons=["order lookup"])
        score, doc = self.store.search(message, k=1)[0]
        return Reply("answer", doc["body"], article_id=doc["id"], score=score)


class SupportAssistant:
    def __init__(self, store=None, customers=None, policy=None, use_llm=False):
        self.store = store or get_store()
        self.customers = customers or load_customers()
        self.policy = policy or PolicyEngine()
        self.use_llm = use_llm

    def respond(self, message, session_email=None):
        if self.policy.is_injection(message):
            return Reply("refuse", REFUSE, reasons=["blocked by injection policy"])

        mentions = find_mentions(message, self.customers)
        if mentions:
            emails_in_msg = {e.lower() for e in EMAIL.findall(message)}
            parts = []
            for c in mentions:
                if session_email and c["email"] == session_email.lower():
                    parts.append(full_record(c))
                elif c["email"] in emails_in_msg and c["order_id"] in message:
                    parts.append(status_only(c))   # guest verification; see README limitations
                else:
                    return Reply("refuse", REFUSE, reasons=["order not owned by requester"])
            return Reply("answer", " ".join(parts), reasons=["verified order lookup"])

        if self.policy.needs_human(message):
            return Reply("handoff", HANDOFF, reasons=["sensitive intent policy"])

        results = self.store.search(message, k=2, expand=True)
        (s1, top), (s2, _) = results[0], results[1]
        margin = (s1 - s2) / s1 if s1 else 0.0
        if s1 < self.policy.gate["min_score"] or margin < self.policy.gate["min_margin"]:
            return Reply("handoff", HANDOFF, score=s1, reasons=[f"low confidence ({s1:.2f}, margin {margin:.2f})"])
        body = top["body"]
        if self.use_llm:
            generated = llm.generate(message, top)
            if generated and generated.strip().upper() == "HANDOFF":
                return Reply("handoff", HANDOFF, score=s1, reasons=["LLM found no answer in the source"])
            body = generated or body
        return Reply("answer", self.policy.redact(f"{body} (Source: {top['title']})"), article_id=top["id"], score=s1)
