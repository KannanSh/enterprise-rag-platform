import time
from app.models.schemas import Citation, RagResponse
from app.providers.factory import get_provider
from app.services.retrieval import search
from app.core.telemetry import GENERATION_LATENCY, RAG_QUERIES

def answer(db, question: str, top_k: int, provider_name: str | None, role: str):
    provider = get_provider(provider_name)
    retrieved = search(db, question, top_k, provider.name)
    context = "\n\n".join(f"[{r['chunk_id']}] {r['title']}: {r['text']}" for r in retrieved)
    prompt = f"Answer only from the supplied context. If the context is insufficient, say so. Cite sources using [chunk_id].\n\nContext:\n{context}\n\nQuestion: {question}"
    start = time.perf_counter(); text = provider.generate(prompt); GENERATION_LATENCY.labels(provider=provider.name).observe(time.perf_counter() - start)
    RAG_QUERIES.labels(provider=provider.name, role=role).inc()
    citations = [Citation(chunk_id=r["chunk_id"], document_id=r["document_id"], title=r["title"], source_uri=r["source_uri"]) for r in retrieved]
    return RagResponse(answer=text, citations=citations, provider=provider.name, retrieved=retrieved)
