from prometheus_client import Counter, Histogram

RAG_QUERIES = Counter("rag_queries_total", "Total RAG queries", ["provider", "role"])
RETRIEVAL_LATENCY = Histogram("rag_retrieval_latency_seconds", "Retrieval latency")
GENERATION_LATENCY = Histogram("rag_generation_latency_seconds", "Generation latency", ["provider"])
DOCUMENTS_INGESTED = Counter("rag_documents_ingested_total", "Documents ingested")
