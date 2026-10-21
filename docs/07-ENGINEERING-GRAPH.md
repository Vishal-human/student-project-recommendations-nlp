# Engineering Graph — Task DAG for Antigravity

> Purpose: give the AI agent ONE node at a time, with a tight, bounded scope, so it never has to
> hold the whole system in context (saves tokens) and never has to guess unspecified behavior
> (prevents hallucination). Feed nodes in the order below. Do not skip ahead — every node lists
> its exact upstream dependencies; nothing later should be started before its dependencies pass
> their "Done when" check.
>
> Rule for the agent operator (you): paste ONLY the single node block below (plus
> `08-DATA-AND-API-CONTRACTS.md` and `09-AGENT-SYSTEM-RULES.md`) into Antigravity for each step.
> Do not paste the whole graph file into the agent's working context at once.

```
N1 (data schema) ──▶ N2 (corpus loader) ──▶ N3 (embedding+index) ──▶ N5 (pipeline)
                                                                          ▲
N4 (feasibility engine) ───────────────────────────────────────────────┘
                                                                          │
N5 (pipeline) ──▶ N6 (API) ──▶ N7 (frontend) ──▶ N8 (docker compose) ──▶ N9 (eval harness)
```

---

### N1 — Data schema
- **Depends on**: nothing (first node)
- **Files to create**: `backend/data/schema.py`
- **Scope**: ONE pydantic model `ProjectEntry` with exactly the fields defined in `08-DATA-AND-API-CONTRACTS.md` §1. Nothing else. No loader logic here.
- **Forbidden**: adding extra fields not in the contract; adding database/ORM code.
- **Done when**: model imports cleanly and validates one sample dict from the contract doc's example.

### N2 — Corpus loader
- **Depends on**: N1
- **Files to create**: `backend/data/loader.py`, `backend/data/sample_corpus.json` (10 rows, matching schema exactly)
- **Scope**: function `load_corpus(path: str) -> list[ProjectEntry]` that reads JSON, validates each row against `ProjectEntry`, raises a clear error on the first invalid row (no silent skipping).
- **Forbidden**: inventing new fields; fetching data from the network; hardcoding a specific real dataset path (must take path as a parameter).
- **Done when**: `load_corpus("backend/data/sample_corpus.json")` returns 10 valid `ProjectEntry` objects.

### N3 — Embedding + vector index
- **Depends on**: N1
- **Files to create**: `backend/ml/index.py`
- **Scope**: exactly two public functions, signatures fixed by `08-DATA-AND-API-CONTRACTS.md` §2:
  `build_index(entries: list[ProjectEntry]) -> FaissIndexWrapper` and
  `query(index: FaissIndexWrapper, text: str, k: int = 5) -> list[MatchResult]`.
  Model: `sentence-transformers/all-MiniLM-L6-v2`, load once at module import, not per call.
- **Forbidden**: any other embedding model; any remote embedding API call; re-embedding the corpus on every query (must embed once at index-build time).
- **Done when**: building an index from the N2 sample corpus and querying with a made-up sentence returns 5 `MatchResult` objects sorted by descending similarity, similarity values in [0,1].

### N4 — Feasibility engine
- **Depends on**: N1
- **Files to create**: `backend/scoring/feasibility.py`, `backend/scoring/rules.yaml`
- **Scope**: exactly one public function, signature fixed by `08-DATA-AND-API-CONTRACTS.md` §3:
  `score_feasibility(student_stack, time_budget_weeks, team_size, topic_tags, complexity_tier) -> FeasibilityResult`.
  All domain→required-skill and complexity-tier mappings live in `rules.yaml`, not hardcoded in Python — this file must be editable without touching code.
- **Forbidden**: any ML model or embedding call in this module (must stay pure rule-based, per PRD §3 non-goals); network calls.
- **Done when**: calling the function with 3 hand-picked test cases (clearly feasible / clearly infeasible / borderline) returns scores and non-empty `reasons` lists that match the expected direction (high/low/medium) for each case.

### N5 — Recommend pipeline
- **Depends on**: N3, N4
- **Files to create**: `backend/pipeline/recommend.py`
- **Scope**: ONE function `recommend(request: RecommendRequest) -> RecommendResponse` (types fixed in contracts doc §4) that:
  1. Calls N3's `query()` against the corpus index using `interests` (or `own_idea` if provided).
  2. For each top match/candidate, calls N4's `score_feasibility()`.
  3. Fills the template-based explanation string (template lives in this file as a plain Python string, no LLM call).
  4. Returns results sorted by a combined rank (novelty then feasibility, simple weighted average — weight constants defined at top of file as named constants, not magic numbers).
- **Forbidden**: calling any LLM/external API; changing N3 or N4 signatures — if a change seems needed, stop and flag it instead of guessing.
- **Done when**: calling `recommend()` with a sample request against the N2 sample corpus returns a valid `RecommendResponse` with 5 non-empty results.

### N6 — API layer
- **Depends on**: N5
- **Files to create**: `backend/main.py`, `backend/Dockerfile`, `backend/requirements.txt`
- **Scope**: FastAPI app with exactly the two endpoints defined in `08-DATA-AND-API-CONTRACTS.md` §5 (`POST /recommend`, `GET /health`). Wire in N5's `recommend()` directly. Enable CORS for `*` in dev only (comment marking it must be restricted before any public deploy).
- **Forbidden**: adding any endpoint not in the contract; adding auth (explicitly out of scope per PRD §3).
- **Done when**: `uvicorn backend.main:app` starts, `GET /health` returns 200, `POST /recommend` with a valid body returns a response matching the contract schema.

### N7 — Frontend
- **Depends on**: N6 (needs the live contract, not the running server — can be built in parallel once N6's contract is fixed, but wire-up/testing needs N6 running)
- **Files to create**: `frontend/index.html`, `frontend/style.css`, `frontend/app.js`
- **Scope**: single page, one form (fields per PRD §5), calls `POST /recommend`, renders result cards per PRD §5. No framework, no build step, no external CSS/JS libraries except plain fetch().
- **Forbidden**: adding routing/multiple pages; adding a JS framework; hardcoding the API base URL (must read from a single `const API_BASE` at top of `app.js`).
- **Done when**: opening `index.html` in a browser (with backend running on localhost) submits the form and renders 5 result cards with all fields from the contract populated.

### N8 — Docker Compose
- **Depends on**: N6, N7
- **Files to create**: `docker-compose.yml`, `frontend/Dockerfile` (nginx static serve), `README.md`
- **Scope**: two services (`backend`, `frontend`), backend on 8000, frontend on 80 proxying `/api/*` to backend. README has exact run instructions and prerequisites.
- **Forbidden**: adding a database service; adding any service not already defined in earlier nodes.
- **Done when**: `docker compose up` from a clean clone serves the working frontend at `localhost` and it successfully calls the backend.

### N9 — Evaluation harness
- **Depends on**: N3 (uses the same index/query function, not a reimplementation)
- **Files to create**: `backend/eval/labeled_pairs.json`, `backend/eval/run_eval.py`, `backend/eval/RESULTS.md`
- **Scope**: 15–20 hand-labeled topic pairs (`{text_a, text_b, is_duplicate: bool}`), a script that runs N3's similarity function on each pair against a chosen threshold, and prints/saves precision/recall/accuracy plus a markdown summary suitable for pasting into the NLP practical report.
- **Forbidden**: modifying N3's index/query logic to make numbers look better — if precision/recall is poor, report it honestly and note it as a limitation (this is expected and normal for a v1 tool with a small corpus).
- **Done when**: `python backend/eval/run_eval.py` runs against the sample corpus and produces `RESULTS.md` with real numbers (even if the sample corpus is tiny and numbers are not impressive yet — that's expected until the real corpus from PRD §10 is in place).

---

## How to swap in the real corpus later
Once the real GLS dataset (PRD §10 open question) is available, only N2's data file changes — replace `sample_corpus.json` with the real file in the same schema, everything else (N3–N9) works unchanged. This is the entire point of building against the contract, not against ad-hoc data.
