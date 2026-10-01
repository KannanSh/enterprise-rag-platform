import json, time
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.auth import Principal, get_principal, require_role
from app.db.session import Base, engine, get_db
from app.models.entities import Document, AuditEvent
from app.models.schemas import DocumentIn, SearchRequest, RagRequest, RetrievalEvaluation
from app.services.audit import record_audit
from app.services.ingestion import ingest
from app.services.retrieval import search
from app.services.rag import answer
from app.services.evaluation import retrieval_metrics

app = FastAPI(title="Enterprise RAG Platform", version="0.1.0")

@app.on_event("startup")
def startup():
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(engine)

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/v1/documents")
def create_document(payload: DocumentIn, principal: Principal = Depends(require_role("analyst")), db: Session = Depends(get_db)):
    try:
        doc = ingest(db, payload.title, payload.source_uri, payload.content)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    record_audit(db, principal.user_id, "document.ingest", doc.id, payload.title)
    return {"id": doc.id, "title": doc.title}

@app.post("/v1/documents/seed")
def seed(principal: Principal = Depends(require_role("admin")), db: Session = Depends(get_db)):
    path = Path("data/knowledge_base.json")
    docs = json.loads(path.read_text())
    created = [ingest(db, d["title"], d["source_uri"], d["content"]) for d in docs]
    record_audit(db, principal.user_id, "document.seed", "knowledge_base", str(len(created)))
    return {"created": len(created)}

@app.post("/v1/search")
def search_endpoint(payload: SearchRequest, principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    results = search(db, payload.query, payload.top_k)
    record_audit(db, principal.user_id, "search", "rag-index", payload.query[:500])
    return {"results": results}

@app.post("/v1/rag/query")
def rag_endpoint(payload: RagRequest, principal: Principal = Depends(get_principal), db: Session = Depends(get_db)):
    try:
        response = answer(db, payload.question if hasattr(payload, "question") else payload.query, payload.top_k, payload.provider, principal.role)
    except Exception as exc:
        raise HTTPException(400, str(exc))
    record_audit(db, principal.user_id, "rag.query", "rag", payload.query[:500])
    return response

@app.post("/v1/evaluations/retrieval")
def eval_endpoint(payload: RetrievalEvaluation, principal: Principal = Depends(require_role("analyst")), db: Session = Depends(get_db)):
    retrieved = search(db, payload.question, 10)
    ids = [r["chunk_id"] for r in retrieved]
    metrics = retrieval_metrics(payload.relevant_chunk_ids, ids)
    record_audit(db, principal.user_id, "evaluation.retrieval", "rag-index", payload.question[:500])
    return {"question": payload.question, "retrieved_chunk_ids": ids, **metrics}

@app.get("/v1/audit")
def audit(principal: Principal = Depends(require_role("admin")), db: Session = Depends(get_db)):
    rows = db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(100).all()
    return [{"id": r.id, "user_id": r.user_id, "action": r.action, "resource": r.resource, "detail": r.detail, "created_at": r.created_at} for r in rows]
