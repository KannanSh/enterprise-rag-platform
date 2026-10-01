from pydantic import BaseModel, Field

class DocumentIn(BaseModel):
    title: str
    source_uri: str
    content: str

class SearchRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = Field(default=4, ge=1, le=20)

class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    source_uri: str = ""
    text: str
    score: float

class RagRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = Field(default=4, ge=1, le=20)
    provider: str | None = None

class Citation(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    source_uri: str

class RagResponse(BaseModel):
    answer: str
    citations: list[Citation]
    provider: str
    retrieved: list[SearchResult]

class RetrievalEvaluation(BaseModel):
    question: str
    relevant_chunk_ids: list[str]
    retrieved_chunk_ids: list[str]
