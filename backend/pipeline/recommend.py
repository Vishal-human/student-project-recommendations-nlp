"""
N5 — Recommend Pipeline
Combines N3 (embedding query) + N4 (feasibility scoring) into a single call.
Exposes: recommend(request: RecommendRequest) -> RecommendResponse

Scoring constants (from 08-DATA-AND-API-CONTRACTS.md §7):
"""
from __future__ import annotations

from pydantic import BaseModel

from data.schema import ProjectEntry
from ml.index import FaissIndexWrapper, MatchResult, query
from scoring.feasibility import score_feasibility

# Scoring weights — named constants, never magic numbers
NOVELTY_WEIGHT = 0.5
FEASIBILITY_WEIGHT = 0.5

# Relevance weight: how strongly the user-query similarity anchors results
# (higher = strongly prefer topics that match what the user asked for)
RELEVANCE_WEIGHT = 0.6


# ---------------------------------------------------------------------------
# Request / Response types (per 08-DATA-AND-API-CONTRACTS.md §4)
# ---------------------------------------------------------------------------

class RecommendRequest(BaseModel):
    interests: str
    stack: list[str]
    time_budget_weeks: int
    team_size: int
    domain_hint: str | None = None
    own_idea: str | None = None


class RecommendationItem(BaseModel):
    title: str
    novelty_score: int
    feasibility_score: int
    explanation: str
    nearest_matches: list[dict]   # [{"title": str, "year": int, "similarity_pct": int}]
    suggested_stack: list[str]
    missing_skills: list[str]


class RecommendResponse(BaseModel):
    recommendations: list[RecommendationItem]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _corpus_novelty(entry: ProjectEntry, index: FaissIndexWrapper) -> tuple[int, list[MatchResult]]:
    """Compute novelty of a corpus entry vs OTHER corpus entries (not vs user query).

    Novelty = how unique is this topic compared to past submissions.
    Queries the index with the entry's own text; the nearest neighbor will be
    itself (similarity ~1.0), so we skip self and use the next closest.
    """
    entry_text = f"{entry.title}. {entry.abstract}"
    neighbors = query(index, entry_text, k=4)
    # Filter out self-match (same id)
    non_self = [r for r in neighbors if r.entry.id != entry.id]
    max_sim = non_self[0].similarity if non_self else 0.0
    novelty = int(round((1.0 - max_sim) * 100))
    return novelty, non_self[:3]


def _combined_rank(relevance_score: float, novelty: int, feasibility: int) -> float:
    """Three-signal rank:
    - relevance_score: how well this topic matches the user's stated interests (0.0-1.0)
    - novelty: how unique it is vs past corpus entries (0-100)
    - feasibility: how buildable it is given the student's stack/time/team (0-100)
    """
    # Normalise relevance to 0-100 to be on the same scale
    relevance_norm = relevance_score * 100
    return (
        RELEVANCE_WEIGHT * relevance_norm
        + (1 - RELEVANCE_WEIGHT) * (NOVELTY_WEIGHT * novelty + FEASIBILITY_WEIGHT * feasibility)
    )


def _make_explanation(
    entry: ProjectEntry,
    novelty: int,
    feasibility: int,
    relevance_pct: int,
    nearest: list[MatchResult],
    missing: list[str],
) -> str:
    nearest_str = nearest[0].entry.title if nearest else "no close matches"
    nearest_sim = int(nearest[0].similarity * 100) if nearest else 0
    miss_str = f" Missing skills: {', '.join(missing)}." if missing else ""
    return (
        f"Relevance {relevance_pct}% match to your interests. "
        f"Novelty {novelty}/100 - closest past project is '{nearest_str}' "
        f"({nearest_sim}% similar, {nearest[0].entry.year if nearest else 'N/A'}).{miss_str} "
        f"Feasibility {feasibility}/100 for your team ({entry.department}, "
        f"{', '.join(entry.tech_stack_tags[:3])})."
    )


def _entry_to_item(
    entry: ProjectEntry,
    relevance_similarity: float,   # similarity between user query and this entry
    index: FaissIndexWrapper,       # needed to compute corpus novelty
    student_stack: list[str],
    time_budget_weeks: int,
    team_size: int,
) -> RecommendationItem:
    # Novelty = uniqueness vs OTHER past projects (not vs user query)
    novelty, corpus_neighbors = _corpus_novelty(entry, index)

    feasibility_result = score_feasibility(
        student_stack=student_stack,
        time_budget_weeks=time_budget_weeks,
        team_size=team_size,
        topic_tags=entry.tech_stack_tags + entry.domain_tags,
        complexity_tier="intermediate",
    )
    nearest_matches = [
        {"title": m.entry.title, "year": m.entry.year, "similarity_pct": int(m.similarity * 100)}
        for m in corpus_neighbors
    ]
    # Scale cosine similarity to a user-friendly percentage.
    # Dense embeddings often top out around 0.5-0.6 for long user query vs short title/abstract.
    # We map 0.2 -> 0% and 0.6 -> 100% so the UI shows intuitive "match" scores.
    scaled_sim = (relevance_similarity - 0.2) / (0.6 - 0.2)
    relevance_pct = int(min(100, max(0, scaled_sim * 100)))

    return RecommendationItem(
        title=entry.title,
        novelty_score=novelty,
        feasibility_score=feasibility_result.score,
        explanation=_make_explanation(
            entry, novelty, feasibility_result.score, relevance_pct,
            corpus_neighbors, feasibility_result.missing_skills
        ),
        nearest_matches=nearest_matches,
        suggested_stack=entry.tech_stack_tags,
        missing_skills=feasibility_result.missing_skills,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def recommend(
    request: RecommendRequest,
    index: FaissIndexWrapper,
    k: int = 5,
) -> RecommendResponse:
    """Run the full recommendation pipeline.

    Step 1: FAISS query retrieves the top semantically RELEVANT entries for
            the user's interests (relevance filter).
    Step 2: For each relevant entry, compute corpus novelty (uniqueness vs
            other past submissions — NOT vs the user query).
    Step 3: Rank by: relevance to query * 0.6 + (novelty + feasibility) * 0.4
            This ensures semantically matching topics rank first, then novelty
            and feasibility break ties.

    If own_idea is provided, scores that idea and returns its 3 nearest corpus
    neighbours as comparison points.
    """
    query_text = request.own_idea if request.own_idea else request.interests

    if request.own_idea:
        # own_idea mode: find closest corpus entries as "similar past projects"
        matches = query(index, query_text, k=3)
        items = []
        for match in matches:
            item = _entry_to_item(
                match.entry, match.similarity, index,
                request.stack, request.time_budget_weeks, request.team_size
            )
            items.append(item)
        return RecommendResponse(recommendations=items[:3])

    # Normal mode: retrieve top relevant matches, then rerank
    # Fetch k*2 so reranking has headroom to reorder
    matches = query(index, query_text, k=min(k * 2, 20))

    scored: list[tuple[float, RecommendationItem]] = []
    for match in matches:
        item = _entry_to_item(
            match.entry, match.similarity, index,
            request.stack, request.time_budget_weeks, request.team_size
        )
        rank = _combined_rank(match.similarity, item.novelty_score, item.feasibility_score)
        scored.append((rank, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return RecommendResponse(recommendations=[item for _, item in scored[:k]])
