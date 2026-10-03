# Architecture Decisions (ADR log)

**Project:** Portfolio Agentic RAG Chatbot
**Status key:** DECIDED = chosen by Waseem. PROPOSED = recommendation, needs approval. OPEN = not decided yet.

---

## ADR-001: LLM provider: Groq (DECIDED)

**Context:** Fast, low-cost inference for a public chatbot.
**Decision:** Use Groq via `langchain-groq`.
**Proposed model setup (verify availability in the Groq console):**
- Generation node: a larger model (e.g. GPT-OSS-120b or a Llama 70B class model).
- Cheap nodes (router, query rewrite, grader): a small model (e.g. GPT-OSS-20b or Llama 3.1 8B).
- Final choice is made with the Phase 3 evaluation, not by guessing.

**Consequences / mitigations:**
- Free-tier rate limits apply per organisation (not per API key), so extra keys do not help.
- Need: per-IP rate limiting, daily request/token budget cap, response caching for repeated questions, and a fallback model (second Groq model, or another provider) if a 429 occurs.
- Check exact limits in Groq Console, Limits page.

---

## ADR-002: Embeddings: Hugging Face, local (DECIDED)

**Decision:** Run embeddings locally with `langchain-huggingface` (`HuggingFaceEmbeddings`).
**Proposed baseline:** `BAAI/bge-small-en-v1.5` (small, fast, low RAM).
**Candidate to compare:** `BAAI/bge-m3` (multilingual, heavier).

**Risk:** Visitors may ask in Roman Urdu while the knowledge base is in English. English-only embeddings retrieve poorly for Roman Urdu queries.
**Mitigation (proposed):** A query-normalisation step in the LangGraph flow: detect language, rewrite the question into a standalone English query for retrieval, answer in the visitor's language.
**Validation:** Phase 3 evaluation includes Roman Urdu questions; compare bge-small + normalisation vs bge-m3.

---

## ADR-003: Vector database: Qdrant, self-hosted with Docker (DECIDED)

**Decision:** Qdrant container in `docker-compose.yml`.
**Requirements:**
- Persistent volume for storage.
- Qdrant API key enabled.
- Port 6333 not exposed to the public internet; only the API container reaches it.
- Periodic snapshot/backup of the collection.
- Ingestion is re-runnable (LangChain Indexing API) so the collection can be rebuilt any time.

---

## ADR-004: Frontend: existing Next.js portfolio (DECIDED)

**Decision:** Add a `ChatWidget` client component (floating button + popup) to the existing Next.js app, mounted once in the root layout.
**Open sub-decision (PROPOSED: direct call for v1):**
- Option A (proposed): browser calls the FastAPI backend directly, CORS restricted to the portfolio domain.
- Option B: browser calls a Next.js route handler that proxies to FastAPI (hides backend URL, no CORS, edge rate limiting), at the cost of extra complexity around streaming.

---

## ADR-005: Backend hosting: AWS EC2 with Docker Compose (PROPOSED)

**Why:** Self-hosted Qdrant, local embeddings and the API need a Docker host with a persistent disk and enough RAM. A single VM running Docker Compose fits this directly.
**Requirements:** HTTPS (domain/subdomain + Caddy or Nginx), firewall allowing only 80/443 (and SSH from own IP), enough RAM for the embedding model + Qdrant + API (size the instance after measuring in Phase 1/2).

---

## ADR-006: Tracing and evaluation (PROPOSED)

- Tracing: Langfuse **cloud free tier** to start. Self-hosting Langfuse adds several extra services (database, cache, storage) and would compete for RAM with Qdrant and embeddings on one VM. Revisit later.
- Evaluation: RAGAS and/or DeepEval, run from `evals/`, wired into CI in Phase 6.

---

## ADR-007: Python tooling (PROPOSED)

- Python 3.11 or 3.12.
- `uv` for environments and dependency locking (fast, reproducible). `pip + venv` is an acceptable fallback.
- `ruff` (lint + format), `pytest`, `pre-commit`.

---

## ADR-008: Agent orchestration and memory (DECIDED/PROPOSED)

- LangChain + LangGraph for the whole RAG and agent flow (DECIDED).
- Session memory via LangGraph checkpointer: SQLite in development, Postgres when deployed (PROPOSED).

---

## ADR-009: Hire/contact notification channel: Email (DECIDED)

**Decision:** The hire/contact tool sends the visitor's name, email and message to Waseem by email.
**Proposed implementation for v1:** SMTP using a dedicated Gmail account with an App Password (needs 2-step verification), stored in environment variables. An email API provider (e.g. Resend) can replace it later if a custom sender domain is wanted.
**Requirements:** validate visitor email format, limit message length, rate limit the tool per IP, set the visitor's address as Reply-To, never put credentials in code.

---

## ADR-010: Backend API framework: FastAPI (DECIDED, agreed in roadmap)

**Decision:** FastAPI (served with Uvicorn) is the backend API of the chatbot.
**Planned endpoints:**
- `POST /chat`: receives the message and session id, runs the LangGraph agent, streams the answer (SSE).
- `POST /feedback`: thumbs up/down linked to a Langfuse trace.
- `GET /health`: health check for deployment and monitoring.

**Why:** async support, native streaming, Pydantic validation, automatic OpenAPI docs, and it fits LangChain/LangGraph well.
**Related libraries:** `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `sse-starlette`, `slowapi` (rate limiting).
**Build phase:** the first version of the API is built in Phase 1 and deployed in Phase 2.

---

## Decision summary

| # | Area | Choice | Status |
|---|---|---|---|
| 001 | LLM | Groq | DECIDED |
| 002 | Embeddings | Hugging Face local (bge-small baseline) | DECIDED / model PROPOSED |
| 003 | Vector DB | Qdrant, Docker self-hosted | DECIDED |
| 004 | Frontend | Next.js ChatWidget | DECIDED |
| 005 | Hosting | AWS EC2 + Docker Compose | PROPOSED |
| 006 | Tracing / eval | Langfuse cloud, RAGAS/DeepEval | PROPOSED |
| 007 | Tooling | Python 3.11+, uv, ruff, pytest | PROPOSED |
| 008 | Memory | LangGraph checkpointer (SQLite then Postgres) | PROPOSED |
| 009 | Notifications | Email (SMTP for v1) | DECIDED |
| 010 | Backend API | FastAPI + Uvicorn | DECIDED |
