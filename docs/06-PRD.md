# PRD — Student Project Topic Recommendation System
Version: 1.0 | Owner: Samarth + partner | Status: Locked for Month-1 build

> This is the single source of truth for WHAT is being built and WHY.
> If any other file (graph, contracts, agent rules) conflicts with this PRD, this PRD wins.
> Do not add features not listed here without updating this file first.

---

## 1. Problem statement
Students picking final-year/practical project topics have no reliable, fast way to check:
(a) whether their topic idea is a near-duplicate of something already submitted at their institution, and
(b) whether it's actually feasible for their team's skills and time budget.
Supervisors currently check this manually (spreadsheets, memory), and generic "AI project idea" blogs and paid project-vendor shops make the duplication problem worse, not better.

## 2. Goal (v1, Month 1)
Ship a working tool where a student enters interests/stack/time/team-size (or their own draft idea) and receives ranked topic recommendations, each with:
- a **novelty score** (semantic similarity vs. a real historical corpus of past project titles),
- a **feasibility score** (rule-based, vs. declared skills/time/team size),
- a **plain-language explanation** for both scores.

## 3. Non-goals (v1) — explicitly OUT of scope, do not build
- No user accounts / auth / login system.
- No payments or monetization.
- No fine-tuned/custom-trained embedding model (use pretrained only — see contracts doc).
- No hosted/paid vector DB (FAISS in-process only).
- No supervisor/admin dashboard (stretch goal only, build last, only if core is done early).
- No multilingual UI (schema must allow a `language` field, but no translation/multilingual matching logic in v1).
- No mobile app.
- No LLM call in the critical scoring path (LLM may ONLY be used, optionally, to rephrase an already-computed explanation — never to compute a score).

## 4. Users
- **Primary**: a student (or 2-person team) picking a project topic.
- **Secondary (future, not v1)**: a supervisor/HOD reviewing submitted topics for overlap.

## 5. Core user flow (v1)
1. Student opens the web page.
2. Student fills a form: `interests` (text), `stack` (multi-select from a fixed tag list), `time_budget_weeks` (int), `team_size` (int), optional `own_idea` (text).
3. Student submits.
4. Backend returns 5 ranked topic recommendations (or, if `own_idea` was given, a score for that idea plus 2 nearby sharper variants).
5. Each result card shows: title, novelty score (0-100), feasibility score (0-100), explanation text, nearest historical matches (title + year + similarity %), suggested stack, missing skills list.
6. Student can read and use this to pick/refine their topic.

## 6. Functional requirements (numbered — each maps to one graph node, see ENGINEERING-GRAPH.md)
- FR1: Load and validate a historical project corpus (CSV/JSON) into a typed structure.
- FR2: Embed corpus text and build a searchable vector index.
- FR3: Given a query string, return top-k nearest historical matches with similarity scores.
- FR4: Given student stack/time/team-size and a candidate topic's requirements, compute a feasibility score + reasons.
- FR5: Combine FR3+FR4 into a single recommend pipeline that also handles the "own_idea" input mode.
- FR6: Expose the pipeline over a REST API (FastAPI).
- FR7: Provide a static HTML/CSS/JS frontend that calls the API and renders results.
- FR8: Containerize both services with Docker Compose, runnable via one command.
- FR9: Provide a small labeled evaluation set + script proving the novelty scorer works (for the NLP practical grade).

## 7. Non-functional requirements
- Must run entirely on free-tier infra (CPU only, no paid API keys required for core function).
- Must return a recommendation response in under ~3 seconds locally for a corpus of a few hundred entries.
- Every score must be explainable/traceable — no black-box numbers in the output.
- Code must run identically for both team members (no hidden local-machine dependencies) — this is why Docker Compose (FR8) is mandatory, not optional.

## 8. Tech stack (locked — do not substitute without updating this file)
- Frontend: HTML + CSS + vanilla JS (no framework, no build step).
- Backend: Python 3.11 + FastAPI + Uvicorn.
- ML: `sentence-transformers` (`all-MiniLM-L6-v2`) + `faiss-cpu`.
- Data: local CSV/JSON file, no external database.
- Infra: Docker + Docker Compose.

## 9. Definition of done (Month 1)
All FR1–FR9 implemented, `docker compose up` runs the full stack from a clean clone, the eval script (FR9) produces a precision/recall summary, and a live demo can go from empty form to scored results in under 10 seconds end to end.

## 10. Open questions (resolve before Week 1 ends — do not let the agent guess these)
- Exact source of the historical corpus (who provides it, what format it arrives in).
- Final fixed list of `stack` tags shown in the frontend multi-select (must match tags used in FR1 data and FR4 rules — see contracts doc, this list must be defined ONCE and reused everywhere).
