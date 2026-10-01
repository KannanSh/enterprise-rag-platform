import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.entities import Chunk, Document
from app.providers.factory import get_provider
from app.core.telemetry import RETRIEVAL_LATENCY

def search(db: Session, query: str, top_k: int, provider_name: str | None = None):
    start = time.perf_counter()
    provider = get_provider(provider_name)
    qv = provider.embed(query)
    distance = Chunk.embedding.cosine_distance(qv).label("distance")
    rows = db.execute(
        select(Chunk, Document, distance)
        .join(Document, Chunk.document_id == Document.id)
        .where(Chunk.embedding.is_not(None))
        .order_by(distance)
        .limit(top_k)
    ).all()
    RETRIEVAL_LATENCY.observe(time.perf_counter() - start)
    return [
        {
            "chunk_id": chunk.id,
            "document_id": doc.id,
            "title": doc.title,
            "source_uri": doc.source_uri,
            "text": chunk.text,
            "score": 1 - float(dist),
        }
        for chunk, doc, dist in rows
    ]
