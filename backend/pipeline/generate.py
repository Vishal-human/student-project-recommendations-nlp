"""
Generate NEW project topics for a student's interests (not retrieved from the corpus).

Pipeline:
  1. Retrieve the nearest existing topics (FAISS) as context, so the generator knows what to avoid.
  2. Generate candidates with an LLM (Google Gemini API) when GEMINI_API_KEY is set,
     otherwise fall back to a simple template remix so the feature still works offline.
  3. Keep only candidates that are NOT too similar to any existing/approved project (embedding check).
  4. Score the survivors with the same relevance / novelty / feasibility logic as recommend().
"""
from __future__ import annotations

import json
import os
import re
import ssl
import urllib.request

import certifi
import numpy as np

from data.tags import TAG_LIST
from ml.index import FaissIndexWrapper, _embed, query
from pipeline.recommend import (
    RecommendationItem,
    RecommendRequest,
    _combined_rank,
)
from scoring.feasibility import score_feasibility

GEN_MODEL = os.getenv("GENERATION_MODEL", "gemini-2.5-flash")
# A generated idea this similar to an existing project is rejected as "not new".
MAX_SIMILARITY_TO_EXISTING = 0.80
MAX_SIMILARITY_BETWEEN_GENERATED = 0.85


class GeneratedItem(RecommendationItem):
    abstract: str = ""
    source: str = "llm"   # "llm" | "template"


class _Candidate:
    def __init__(self, title: str, abstract: str, tags: list[str]) -> None:
        self.title = title.strip()
        self.abstract = abstract.strip()
        self.tags = [t for t in tags if t in TAG_LIST]


# ---------------------------------------------------------------------------
# Candidate generation
# ---------------------------------------------------------------------------

def _llm_candidates(req: RecommendRequest, avoid_titles: list[str], n: int) -> list[_Candidate]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    prompt = (
        f"You help college students pick final-year project topics.\n"
        f"Student interests: {req.interests}\n"
        f"Tech stack they know: {', '.join(req.stack) or 'not specified'}\n"
        f"Time: {req.time_budget_weeks} weeks, team size: {req.team_size}\n\n"
        f"Propose {n} NEW, specific, buildable project topics in these interests. "
        f"They must be clearly different from every project below (not paraphrases):\n"
        + "\n".join(f"- {t}" for t in avoid_titles)
        + f"\n\nReply with ONLY a JSON array of {n} objects: "
        '{"title": str, "abstract": str (1-2 sentences), "tech_stack": [tags]}. '
        f"tech_stack tags must come from: {', '.join(TAG_LIST)}."
    )
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.9},
    }).encode()
    http_req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEN_MODEL}:generateContent",
        data=body,
        headers={"x-goog-api-key": api_key, "content-type": "application/json"},
    )
    ctx = ssl.create_default_context(cafile=certifi.where())   # macOS Python lacks system CA certs
    with urllib.request.urlopen(http_req, timeout=40, context=ctx) as resp:
        text = json.loads(resp.read())["candidates"][0]["content"]["parts"][0]["text"]
    rows = json.loads(re.search(r"\[.*\]", text, re.S).group(0))
    return [_Candidate(r["title"], r.get("abstract", ""), r.get("tech_stack", [])) for r in rows]


def _template_candidates(req: RecommendRequest, neighbours, n: int) -> list[_Candidate]:
    """Offline fallback: remix domains/tech of nearby topics with the student's own stack."""
    domains: list[str] = []
    for m in neighbours:
        for d in m.entry.domain_tags:
            if d not in domains:
                domains.append(d)
    domains = domains or ["education"]
    stack = [s for s in req.stack if s in TAG_LIST] or ["python"]
    interest = req.interests.strip().rstrip(".") or "your interest area"
    patterns = [
        ("Smart {d} Assistant with Personalised Insights", "An assistant for {d} that personalises results using {i}."),
        ("Real-Time {d} Monitoring Dashboard", "A live dashboard for {d} that tracks and visualises data related to {i}."),
        ("Explainable {d} Recommender for Students", "A recommender in {d} that explains why each suggestion fits {i}."),
        ("{d} Early-Warning System using Analytics", "Predicts problems early in {d} using data analysis around {i}."),
        ("Collaborative {d} Platform with Smart Matching", "Matches users in {d} by shared goals related to {i}."),
    ]
    out = []
    for k in range(n):
        d = domains[k % len(domains)].replace("-", " ").title()
        t, a = patterns[k % len(patterns)]
        out.append(_Candidate(t.format(d=d), a.format(d=d, i=interest), stack[:3]))
    return out


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_topics(
    req: RecommendRequest,
    index: FaissIndexWrapper,
    approved_titles: list[str],
    n: int = 5,
) -> tuple[str, list[GeneratedItem], str]:
    """Return (source, items, fallback_reason). Items are new topics, ranked, each unique vs the corpus."""
    neighbours = query(index, req.interests, k=10)
    avoid = [m.entry.title for m in neighbours] + approved_titles[:10]

    try:
        candidates = _llm_candidates(req, avoid, n + 3)
        source, reason = "llm", ""
    except Exception as exc:
        candidates = _template_candidates(req, neighbours, n + 3)
        source, reason = "template", f"{type(exc).__name__}: {exc}"[:160]

    if not candidates:
        return source, [], reason

    cand_vecs = _embed([f"{c.title}. {c.abstract}" for c in candidates])
    query_vec = _embed([req.interests])[0]
    approved_vecs = _embed(approved_titles) if approved_titles else None

    kept: list[tuple[float, GeneratedItem]] = []
    kept_vecs: list[np.ndarray] = []
    for c, vec in zip(candidates, cand_vecs):
        near = query(index, f"{c.title}. {c.abstract}", k=3)
        max_sim = near[0].similarity if near else 0.0
        if max_sim >= MAX_SIMILARITY_TO_EXISTING:
            continue                                   # too close to a past project
        if approved_vecs is not None and float(np.max(approved_vecs @ vec)) >= MAX_SIMILARITY_TO_EXISTING:
            continue                                   # too close to an already-approved topic
        if any(float(vec @ kv) >= MAX_SIMILARITY_BETWEEN_GENERATED for kv in kept_vecs):
            continue                                   # duplicate of another generated idea

        novelty = int(round((1.0 - max_sim) * 100))
        feas = score_feasibility(
            student_stack=req.stack,
            time_budget_weeks=req.time_budget_weeks,
            team_size=req.team_size,
            topic_tags=c.tags,
            complexity_tier="intermediate",
        )
        relevance = float(vec @ query_vec)
        relevance_pct = int(min(100, max(0, (relevance - 0.2) / 0.4 * 100)))
        explanation = (
            f"{c.abstract} Relevance {relevance_pct}% to your interests. "
            f"Novelty {novelty}/100 - closest existing project is "
            f"'{near[0].entry.title if near else 'none'}' ({int(max_sim * 100)}% similar). "
            f"Feasibility {feas.score}/100 for your team."
        )
        item = GeneratedItem(
            title=c.title,
            novelty_score=novelty,
            feasibility_score=feas.score,
            explanation=explanation,
            nearest_matches=[
                {"title": m.entry.title, "year": m.entry.year, "similarity_pct": int(m.similarity * 100)}
                for m in near
            ],
            suggested_stack=c.tags or req.stack,
            missing_skills=feas.missing_skills,
            abstract=c.abstract,
            source=source,
        )
        kept.append((_combined_rank(max(0.0, relevance), novelty, feas.score), item))
        kept_vecs.append(vec)

    kept.sort(key=lambda x: x[0], reverse=True)
    return source, [item for _, item in kept[:n]], reason
