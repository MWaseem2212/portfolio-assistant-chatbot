# Requirements: Portfolio Agentic RAG Chatbot

**Owner:** Muhammad Waseem
**Status:** Draft v1 (Phase 0, Step 0.1)
**Last updated:** 2026-10-01

## 1. Overview

A visitor-facing chatbot embedded in the portfolio website. Visitors open it from a floating button and ask anything about Waseem: projects, skills, experience, resume, contact details. Answers come only from a curated knowledge base (Agentic RAG with LangChain + LangGraph), so the bot does not hallucinate. It is also a showcase of production-grade GenAI engineering: evaluation, tracing, guardrails, CI/CD.

## 2. Users and what they ask

| User | Typical questions |
|---|---|
| Recruiter / HR | Experience, skills, resume, availability, contact |
| Client | What have you built, can you build X, how to hire |
| Engineer / peer | Architecture, tech stack, project details, GitHub links |

## 3. Functional requirements

| ID | Requirement |
|---|---|
| FR1 | Answer questions about projects, skills, experience, education, resume and contact using only the knowledge base. |
| FR2 | Reply in the visitor's language: English if asked in English, Roman Urdu if asked in Roman Urdu. |
| FR3 | Professional tone in every reply. |
| FR4 | Contact details (email, phone, LinkedIn, GitHub) are returned through normal retrieval from the knowledge base (`contact.md`). |
| FR5 | A hire/contact tool collects the visitor's name, email and message and forwards it to Waseem (email or Telegram). |
| FR6 | Provide the resume download link on request. |
| FR7 | If the answer is not in the knowledge base, say so clearly and suggest the contact tool. Never guess. |
| FR8 | Show the source (document/section) for factual answers. |
| FR9 | Politely decline off-topic requests (general knowledge, coding help, questions about other people). |
| FR10 | Remember the conversation within a session (follow-up questions work). |
| FR11 | Stream answers token by token. |
| FR12 | Thumbs up / down feedback on each answer, linked to its trace. |

## 4. Non-functional requirements

| Area | Requirement |
|---|---|
| Latency | First token quickly (target: under 5 s). |
| Cost | Hard daily budget cap on LLM usage. |
| Security | API keys only in backend environment variables. CORS restricted to the portfolio domain. HTTPS only. |
| Abuse protection | Per-IP rate limiting, message length limit, prompt-injection defences. |
| Observability | Every request traced (latency, tokens, cost, node inputs/outputs). |
| Quality | Automated evaluation on a golden dataset; CI fails if scores drop. |
| Reliability | Health endpoint and a fallback model if the primary LLM is down. |
| Maintainability | Knowledge base re-indexable with one command when the resume or projects change. |
| Privacy | Visitor messages are stored only for traces and evaluation; no unnecessary personal data. |

## 5. Non-goals

- General-purpose assistant (trivia, news, coding help).
- Talking about people other than Waseem.
- Making commitments on Waseem's behalf (salary, contracts, availability) beyond what is written in the knowledge base.
- Voice or multimodal input (not in v1).

## 6. Success criteria (proposed targets, to be confirmed after Phase 3 baseline)

- Faithfulness (RAGAS) of 0.9 or higher on the golden dataset.
- Correct "I don't know" behaviour on unanswerable questions.
- All adversarial test prompts (injection, prompt leak, off-topic) rejected.
- Live on the portfolio with tracing and a monitoring dashboard.

## 7. Knowledge base scope

`about.md`, `skills.md`, `experience.md`, `education.md`, `projects/*.md` (DocuMind AI, NexaAgent, Resume Matcher, OpsPilot), `contact.md`, `faq.md`, `resume.pdf`.

## 8. Open decisions (to be closed in Step 0.2)

- [ ] LLM provider
- [ ] Embedding model
- [ ] Vector DB hosting (Qdrant Cloud vs self-hosted)
- [ ] Backend hosting (EC2 vs Render/Railway)
- [ ] Portfolio frontend framework
- [ ] Notification channel for the hire/contact tool (email vs Telegram)
