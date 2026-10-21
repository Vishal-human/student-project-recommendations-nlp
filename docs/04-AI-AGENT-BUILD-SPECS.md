# AI Agent Build Specs (Antigravity IDE / spec-driven)

Use these as separate spec docs fed to your AI coding agent, one per module — matching the phased spec-pack methodology you already used on your Sentence-BERT/FAISS/FastAPI prototype and your CodeAlpha projects.

---

## SPEC 1 — Data Layer

**Persona to load**: CTO
**Prompt skeleton**:
```
Act as a CTO reviewing a data schema for a student project-topic recommendation system.
Build a Python module that:
1. Loads a CSV/JSON of past project entries with fields:
   title, abstract, year, department, tech_stack_tags (list), domain_tags (list), language (default "en")
2. Validates and cleans text (strip, lowercase-normalize for matching only, keep original for display)
3. Exposes a function `load_corpus(path) -> List[ProjectEntry]` using a typed dataclass/pydantic model
4. Includes a small synthetic sample dataset (10 rows) for testing before the real dataset is ready
Output: data/schema.py, data/loader.py, data/sample_corpus.json
```

## SPEC 2 — Embedding + Vector Index

**Persona to load**: ML/Fine-tuning Lead
**Prompt skeleton**:
```
Act as an ML engineer specializing in sentence embeddings and vector search.
Build a Python module using sentence-transformers ("all-MiniLM-L6-v2") and FAISS that:
1. Embeds a list of ProjectEntry title+abstract pairs
2. Builds and persists a FAISS IndexFlatIP (cosine via normalized vectors)
3. Exposes `build_index(entries) -> FaissIndexWrapper` and
   `query(text: str, k: int = 5) -> List[(ProjectEntry, similarity_score)]`
4. Include a CLI test: embed the sample corpus, query with a made-up topic, print top-5 matches with scores
Constraints: CPU-only, no external API calls, must run inside a lightweight Docker image.
```

## SPEC 3 — Feasibility Scoring Engine

**Persona to load**: EdTech Strategist + CTO (joint review)
**Prompt skeleton**:
```
Act as a CTO and EdTech strategist designing a transparent, rule-based feasibility scorer
(explicitly NOT a black-box ML model — every score must be traceable to a rule).
Build a Python module that takes:
- student_stack: List[str] (e.g. ["javascript","python","docker"])
- time_budget_weeks: int
- team_size: int
- candidate topic's tech_stack_tags and a manually curated complexity_tier ("beginner"/"intermediate"/"advanced")
and returns a feasibility_score (0-100) plus a list of human-readable reasons
(e.g. "Missing skill: OpenCV for computer vision component", "Tight on time: advanced-tier topic with 2-week budget").
Include a small YAML/JSON config file mapping domain tags -> typical required skills and complexity tier,
so non-engineers (e.g. the EdTech/product side of the team) can edit scoring rules without touching code.
```

## SPEC 4 — API Layer

**Persona to load**: CTO
**Prompt skeleton**:
```
Act as a CTO defining a clean API contract.
Build a FastAPI app with:
POST /recommend
  body: { interests: str, stack: [str], time_budget_weeks: int, team_size: int, domain_hint: str|null, own_idea: str|null }
  returns: { recommendations: [ { title, novelty_score, feasibility_score, nearest_matches: [{title, year, similarity}], explanation, suggested_stack, missing_skills } ] }
GET /health
Wire in the embedding/index module (Spec 2) and feasibility module (Spec 3).
Include CORS for local frontend dev, Pydantic request/response models, and basic input validation
(reject empty interests, cap k at 10).
Add a Dockerfile and confirm it runs on port 8000 with `uvicorn`.
```

## SPEC 5 — Frontend

**Persona to load**: EdTech Strategist (UX for students) + frontend engineer
**Prompt skeleton**:
```
Act as a frontend engineer building a clean, fast, no-framework HTML/CSS/JS UI (single page) that:
1. Has a form: interests (textarea), stack (multi-select chips), time budget (weeks, number),
   team size (number), optional "I already have an idea" text field
2. On submit, calls POST /recommend and renders results as cards: title, novelty score
   (color-coded: green >70, yellow 40-70, red <40), feasibility score (same coding),
   plain-language explanation, nearest matches as a collapsible detail
3. Loading and error states must be handled (spinner, friendly error message)
4. Keep it lightweight (no build step required) so it can be served as a static file inside Docker/nginx.
Style: clean academic-tool feel, not flashy — this needs to look credible to a HOD, not like a hackathon toy.
```

## SPEC 6 — Docker Compose

**Persona to load**: CTO
**Prompt skeleton**:
```
Act as a CTO finalizing deployment. Write a docker-compose.yml with two services:
- backend: builds from the FastAPI Dockerfile, exposes 8000, mounts the corpus data volume
- frontend: nginx serving the static HTML/CSS/JS, exposes 80, proxies /api to backend
Include a README with exact `docker compose up` instructions and a note on which free-tier host
(Render/Railway) this is verified to deploy on, matching the team's existing free-tier deployment pattern.
```

## SPEC 7 — Evaluation Set (for your NLP practical report)

**Persona to load**: ML/Fine-tuning Lead
**Prompt skeleton**:
```
Act as an ML engineer building a lightweight evaluation harness.
Create a hand-labeled set of 15-20 topic pairs (some clearly duplicate/near-duplicate,
some clearly novel) drawn from or inspired by the real corpus.
Write a script that runs the novelty scorer against these pairs and reports:
- accuracy of correctly flagging duplicates above a chosen similarity threshold
- a simple precision/recall table
- a short markdown summary suitable for pasting into an academic report's "Evaluation" section
```

---

### How to use these day-to-day
Feed one spec at a time to your agent inside Antigravity, review the diff, run the built-in checkpoint test noted in each spec before moving to the next — this mirrors exactly the phased/graph-prompted workflow you used successfully on PULSE, CarbonZero, and your CodeAlpha internship projects, so no new process needs to be learned.
