from sqlalchemy.orm import Session
from app.models.entities import Document, Chunk
from app.providers.factory import get_provider
from app.core.telemetry import DOCUMENTS_INGESTED

def chunk_text(text: str, size: int = 700):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)] or [""]

def ingest(db: Session, title: str, source_uri: str, content: str, provider_name: str | None = None):
    provider = get_provider(provider_name)
    doc = Document(title=title, source_uri=source_uri, content=content)
    db.add(doc); db.flush()
    for idx, text in enumerate(chunk_text(content)):
        db.add(Chunk(document_id=doc.id, chunk_index=idx, text=text, embedding=provider.embed(text)))
    db.commit(); DOCUMENTS_INGESTED.inc()
    return doc
