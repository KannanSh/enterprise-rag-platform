# Enterprise RAG Platform

A production-oriented reference implementation of an enterprise Retrieval-Augmented Generation (RAG) platform designed for cloud architecture, AI engineering, security, governance, and DevOps portfolios.

**Focus:** Python • FastAPI • PostgreSQL/pgvector • RAG • citations • RBAC • audit trail • evaluation • Docker • Terraform • Prometheus/Grafana • OpenAI/Azure OpenAI/AWS Bedrock provider abstraction

> Portfolio note: this repository is a reference implementation and local demonstration. Cloud Terraform is intentionally foundational; production deployment still requires environment-specific networking, identity, secrets, data-protection, and operational controls.

## Architecture

```text
                         +---------------------------+
                         |        Client / UI         |
                         +-------------+-------------+
                                       |
                                  REST / JSON
                                       |
                         +-------------v-------------+
                         |         FastAPI            |
                         | auth • RBAC • audit        |
                         +------+------+--------------+
                                |      |
                    +-----------+      +----------------+
                    |                                  |
             +------v------+                    +------v------+
             | RAG Service |                    | Evaluation  |
             | retrieve    |                    | metrics     |
             | rerank      |                    +-------------+
             | cite        |
             +------+------+ 
                    |
             +------v-----------------------------+
             | PostgreSQL + pgvector              |
             | documents • chunks • embeddings   |
             | audit events • evaluation runs    |
             +------+-----------------------------+
                    |
             +------v-----------------------------+
             | LLM / Embedding Provider           |
             | OpenAI | Azure OpenAI | Bedrock    |
             +------------------------------------+

 Observability: Prometheus metrics -> Grafana
 Deployment: Docker Compose locally; Terraform foundations for AWS/Azure
```

## What is implemented

- FastAPI API for health, document ingestion, search and RAG query.
- PostgreSQL + pgvector schema for documents/chunks/embeddings.
- Provider abstraction for OpenAI, Azure OpenAI and AWS Bedrock.
- Deterministic local embeddings and answer mode for offline demos.
- Citation-aware answers that expose source document/chunk IDs.
- Simple RBAC (`admin`, `analyst`, `viewer`) with API-key authentication for the demo.
- Append-only audit events for access and query activity.
- Evaluation service with retrieval precision/recall and citation coverage.
- Prometheus metrics endpoint.
- Docker Compose for API + PostgreSQL + Prometheus + Grafana.
- Terraform foundations for AWS and Azure deployment patterns.
- Tests covering retrieval, RBAC and evaluation behavior.

## Quick start

### 1. Start services

```bash
docker compose up --build
```

API: http://localhost:8000/docs  
Metrics: http://localhost:8000/metrics  
Prometheus: http://localhost:9090  
Grafana: http://localhost:3000

### 2. Seed demo knowledge

```bash
curl -X POST http://localhost:8000/v1/documents/seed \
  -H "X-API-Key: demo-admin"
```

### 3. Query the RAG system

```bash
curl -X POST http://localhost:8000/v1/rag/query \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: demo-analyst' \
  -d '{"question":"What is the cloud backup retention policy?","top_k":4}'
```

The default `LOCAL` provider makes this runnable without external API keys. Configure an external provider when you want real LLM generation.

## Provider configuration

### OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.1
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

### Azure OpenAI

```env
LLM_PROVIDER=azure_openai
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-10-21
AZURE_OPENAI_DEPLOYMENT=YOUR_CHAT_DEPLOYMENT
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=YOUR_EMBEDDING_DEPLOYMENT
```

### AWS Bedrock

```env
LLM_PROVIDER=bedrock
AWS_REGION=eu-central-1
BEDROCK_MODEL_ID=YOUR_MODEL_ID
BEDROCK_EMBEDDING_MODEL_ID=YOUR_EMBEDDING_MODEL_ID
```

Provider APIs change over time; verify model IDs, SDK parameters and regional availability before production deployment.

## API endpoints

| Endpoint | Purpose | Role |
|---|---|---|
| `GET /health` | health check | public |
| `GET /metrics` | Prometheus metrics | public |
| `POST /v1/documents` | ingest a document | admin/analyst |
| `POST /v1/documents/seed` | load demo documents | admin |
| `POST /v1/search` | retrieve chunks | viewer+ |
| `POST /v1/rag/query` | answer with citations | viewer+ |
| `POST /v1/evaluations/retrieval` | evaluate retrieval | analyst+ |
| `GET /v1/audit` | inspect audit events | admin |

## Evaluation

The evaluation module supports a small, transparent benchmark format:

```json
{
  "question": "What is the backup retention policy?",
  "relevant_chunk_ids": ["chunk-id-1"],
  "retrieved_chunk_ids": ["chunk-id-1", "chunk-id-2"]
}
```

It calculates retrieval precision, recall and F1, plus citation coverage for generated answers. This is deliberately simple enough to understand and extend with RAGAS/DeepEval or a custom enterprise benchmark later.

## Security / governance design

The implementation demonstrates:

- Role-based authorization before sensitive operations.
- Audit records for authenticated actions.
- Source-level citations to improve traceability.
- Provider abstraction so credentials remain outside business logic.
- Configuration via environment variables rather than hard-coded secrets.
- Clear separation between retrieval, generation and policy concerns.

For production, add enterprise IAM/OIDC, short-lived credentials, secret managers, tenant isolation, encryption/key management, PII controls, prompt-injection defenses, content safety, network isolation, policy-as-code and formal threat modeling.

## Repository structure

```text
app/
  api/            FastAPI routes
  core/           configuration, auth, telemetry
  db/             SQLAlchemy session and schema initialization
  models/         ORM models and API schemas
  providers/      local/OpenAI/Azure OpenAI/Bedrock adapters
  services/       ingestion, retrieval, RAG and evaluation
infra/terraform/  cloud deployment foundations
monitoring/       Prometheus/Grafana configuration
data/             demo knowledge base
tests/            automated tests
docker-compose.yml
Dockerfile
```

## Portfolio talking points

This project is designed to demonstrate architecture decisions that are relevant to Senior/Principal Cloud & AI Architect roles:

1. **AI architecture:** RAG pipeline, embeddings, retrieval, generation and citations.
2. **Cloud architecture:** provider abstraction across AWS, Azure and OpenAI ecosystems.
3. **Enterprise security:** RBAC, auditability and a clear path to enterprise identity.
4. **Operational excellence:** metrics, health checks, containers and infrastructure-as-code.
5. **Governance:** traceable source references and evaluation metrics.
6. **Engineering maturity:** tests, typed schemas, modular services and explicit production gaps.

## License

MIT
