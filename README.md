# Portfolio Assistant Chatbot

A production-grade Agentic RAG chatbot for my portfolio. Visitors can ask about my projects, skills, experience, resume and contact details; answers come only from a curated knowledge base.

**Status:** Phase 0 (foundation)

## Stack
LangChain + LangGraph, Groq, Hugging Face embeddings (local), Qdrant (Docker), FastAPI, Langfuse, Next.js widget.

## Docs
- [Requirements](docs/requirements.md)
- [Architecture decisions](docs/decisions.md)

## Setup
_To be completed as phases progress._

## Project structure
```
app/          FastAPI app, LangGraph agent, retrieval, guardrails, tools
data/raw/     Knowledge base (markdown + resume)
data/eval/    Golden evaluation dataset
scripts/      Ingestion and utility scripts
evals/        Evaluation runs
tests/        Unit and integration tests
frontend/     Chat widget for the Next.js portfolio
docs/         Requirements and decisions
```
