"""LLM microservice API (FastAPI).

Run:   uvicorn app.api:app --reload
Try:   curl -X POST localhost:8000/chat -H "Content-Type: application/json" \
            -d '{"message": "How do I reset my password?"}'
"""
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from . import config
from .assistant import SupportAssistant

app = FastAPI(title="RAG Support Service", version="1.0.0",
              description="Grounded answers, human handoff and data-leak protection for customer support.")
assistant = SupportAssistant()


class ChatRequest(BaseModel):
    message: str
    session_email: Optional[str] = None


class ChatResponse(BaseModel):
    action: str
    text: str
    article_id: Optional[str] = None
    score: float
    reasons: list


@app.get("/health")
def health():
    return {"status": "ok", "store": config.STORE_BACKEND, "articles": len(assistant.store.docs),
            "policy_version": assistant.policy.policy["version"]}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    r = assistant.respond(req.message, req.session_email)
    return ChatResponse(action=r.action, text=r.text, article_id=r.article_id, score=round(r.score, 3), reasons=r.reasons)
