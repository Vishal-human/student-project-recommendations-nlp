# Data & API Contracts — LOCKED

> Every field name, type, and endpoint shape below is FINAL for v1.
> The agent must use these exact names — never invent, rename, pluralize, or "improve" a field name.
> If a node seems to need a field not listed here, STOP and flag it as an open question
> rather than inventing one. This file exists specifically to stop drift/hallucination across
> multiple separate agent sessions building different nodes.

---

## 1. `ProjectEntry` (historical corpus row) — used by N1, N2, N3

```python
class ProjectEntry(BaseModel):
    id: str                      # stable unique id, e.g. "gls-2023-041"
    title: str
    abstract: str                # 1-3 sentence summary; if unavailable, repeat title
    year: int
    department: str              # e.g. "IMCA"
    tech_stack_tags: list[str]   # MUST come from the fixed TAG_LIST in §6, lowercase
    domain_tags: list[str]       # free-ish but lowercase, e.g. ["healthcare","nlp"]
    language: str = "en"         # ISO 639-1, default "en", not used for matching in v1
```

Example:
```json
{
  "id": "gls-2023-041",
  "title": "AI-Based Resume Screening Tool",
  "abstract": "A tool that screens resumes against job descriptions using NLP techniques.",
  "year": 2023,
  "department": "IMCA",
  "tech_stack_tags": ["python", "nlp", "flask"],
  "domain_tags": ["hr-tech", "nlp"],
  "language": "en"
}
```

## 2. Embedding/index types — used by N3, N5

```python
class MatchResult(BaseModel):
    entry: ProjectEntry
    similarity: float   # cosine similarity, range 0.0–1.0, NOT percentage

class FaissIndexWrapper:
    # opaque wrapper object holding: the faiss.Index, the parallel list[ProjectEntry],
    # and the loaded SentenceTransformer model reference. No public fields required
    # beyond what build_index()/query() need internally.
    pass
```

Function signatures (exact, do not change):
```python
def build_index(entries: list[ProjectEntry]) -> FaissIndexWrapper: ...
def query(index: FaissIndexWrapper, text: str, k: int = 5) -> list[MatchResult]: ...
```

## 3. Feasibility types — used by N4, N5

```python
class FeasibilityResult(BaseModel):
    score: int              # 0-100 integer
    reasons: list[str]      # human-readable, at least 1 item, e.g. "Missing skill: opencv"
    missing_skills: list[str]  # subset of TAG_LIST, may be empty
```

Function signature (exact):
```python
def score_feasibility(
    student_stack: list[str],
    time_budget_weeks: int,
    team_size: int,
    topic_tags: list[str],
    complexity_tier: str,   # one of "beginner" | "intermediate" | "advanced"
) -> FeasibilityResult: ...
```

## 4. API request/response types — used by N5, N6, N7

```python
class RecommendRequest(BaseModel):
    interests: str
    stack: list[str]              # subset of TAG_LIST (§6)
    time_budget_weeks: int
    team_size: int
    domain_hint: str | None = None
    own_idea: str | None = None   # if present, score THIS idea instead of generating fresh ones

class RecommendationItem(BaseModel):
    title: str
    novelty_score: int            # 0-100 integer (converted from similarity: see N5 formula)
    feasibility_score: int        # 0-100 integer, directly from FeasibilityResult.score
    explanation: str              # plain-language, template-generated
    nearest_matches: list[dict]   # [{ "title": str, "year": int, "similarity_pct": int }], max 3 items
    suggested_stack: list[str]    # subset of TAG_LIST
    missing_skills: list[str]     # from FeasibilityResult.missing_skills

class RecommendResponse(BaseModel):
    recommendations: list[RecommendationItem]   # exactly 5 items in v1, unless own_idea given (then 3: the idea + 2 variants)
```

## 5. REST endpoints — used by N6, N7

```
POST /recommend
  Request body: RecommendRequest (JSON)
  Response body: RecommendResponse (JSON)
  Errors:
    400 if interests is empty AND own_idea is empty
    400 if time_budget_weeks <= 0 or team_size <= 0
    422 on schema validation failure (default FastAPI behavior, do not override)

GET /health
  Response: { "status": "ok" }
```

No other endpoints exist in v1. Do not add `/topics`, `/corpus`, `/admin`, etc. — those are explicitly out of scope per PRD §3.

## 6. Fixed tag list — `TAG_LIST` — used EVERYWHERE (N1, N2, N4, N7)

> This list must be defined in exactly ONE place — `backend/data/tags.py` as a plain Python list
> of strings — and imported everywhere else (including referenced/copied into the frontend's
> multi-select in N7). Never redefine this list in a second location.

```python
TAG_LIST = [
    "javascript", "typescript", "python", "html", "css",
    "react", "nodejs", "fastapi", "flask", "django",
    "docker", "sql", "mongodb", "firebase",
    "nlp", "computer-vision", "machine-learning", "deep-learning",
    "data-analysis", "api-integration",
]
```
(This list may be edited ONCE at project start if the team wants different tags — but after N1 is built, it is locked for the rest of the build to avoid every downstream node needing rework.)

## 7. Scoring constants — used by N5

```python
NOVELTY_WEIGHT = 0.5
FEASIBILITY_WEIGHT = 0.5
# combined_rank = NOVELTY_WEIGHT * novelty_score + FEASIBILITY_WEIGHT * feasibility_score
# novelty_score = round((1 - top_similarity) * 100), clipped to [0, 100]
```

---

## Why this file exists
Multi-session AI-agent builds hallucinate most often by silently renaming fields or inventing new ones between sessions (e.g. `novelty_score` becomes `noveltyScore` or `score_novelty` in a later file). Every node spec in `07-ENGINEERING-GRAPH.md` must be built by copy-checking field names against this file, not from memory of an earlier conversation turn.
