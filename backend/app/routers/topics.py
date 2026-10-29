"""
N6 — Topics router
POST /recommend   — NLP recommendations, filters out approved/taken topics
GET  /topics/domains — domain overview
"""
import sys
import json
from collections import Counter
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ProjectProposal, User
from app.deps import get_current_user

router = APIRouter(prefix="/topics", tags=["topics"])

# ---------------------------------------------------------------------------
# Static topic dataset for domain overview
# ---------------------------------------------------------------------------
_TOPICS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "topics.json"
with open(_TOPICS_PATH) as f:
    _TOPICS = json.load(f)

# ---------------------------------------------------------------------------
# NLP pipeline — corpus + FAISS index built once at module import
# ---------------------------------------------------------------------------
_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from data.loader import load_corpus
from ml.index import build_index, _embed, query as faiss_query
from pipeline.recommend import recommend, RecommendRequest, RecommendResponse
from pipeline.generate import generate_topics, GeneratedItem
from pydantic import BaseModel

import faiss
import numpy as np

_CORPUS_PATH = _BACKEND_ROOT / "data" / "sample_corpus.json"
_corpus = load_corpus(str(_CORPUS_PATH))
_index = build_index(_corpus)

# Similarity threshold below which a recommendation is considered "taken"
_TAKEN_THRESHOLD = 0.82


def _get_approved_titles(db: Session) -> list[str]:
    """Fetch all approved project titles from the DB."""
    rows = db.query(ProjectProposal.title).filter(ProjectProposal.status == "approved").all()
    return [r.title for r in rows]


def _filter_taken(recommendations, approved_titles: list[str]):
    """Remove recommendations that are semantically too close to any approved title."""
    if not approved_titles:
        return recommendations
    approved_vecs = _embed(approved_titles)
    # Build a tiny index of approved titles for fast comparison
    dim = approved_vecs.shape[1]
    approved_index = faiss.IndexFlatIP(dim)
    approved_index.add(approved_vecs)

    filtered = []
    for item in recommendations:
        vec = _embed([item.title])
        dists, _ = approved_index.search(vec, k=1)
        max_sim = float(np.clip(dists[0][0], 0.0, 1.0))
        if max_sim < _TAKEN_THRESHOLD:
            filtered.append(item)
    return filtered


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/domains")
def list_domains(current_user: User = Depends(get_current_user)):
    """Domain names + topic counts from the corpus dataset."""
    counts = Counter(topic["domain"] for topic in _TOPICS)
    return {
        "total_topics": len(_TOPICS),
        "domains": [{"domain": d, "count": c} for d, c in sorted(counts.items())],
    }


@router.post("/recommend", response_model=RecommendResponse)
def get_recommendations(
    body: RecommendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """NLP-powered recommendations.

    Automatically filters out topics already approved for other students —
    so we never recommend a 'taken' idea.
    """
    if not body.interests and not body.own_idea:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Provide at least one of: interests, own_idea")
    if body.time_budget_weeks <= 0 or body.team_size <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="time_budget_weeks and team_size must be > 0")

    # Fetch a large batch so we have enough left after filtering taken topics
    response = recommend(body, _index, k=20)

    # Filter out taken topics
    approved_titles = _get_approved_titles(db)
    response.recommendations = _filter_taken(response.recommendations, approved_titles)

    # Now return the top 5 available topics
    response.recommendations = response.recommendations[:5]

    return response


class GenerateResponse(BaseModel):
    source: str          # "llm" (Gemini) or "template" (offline fallback)
    notice: str
    recommendations: list[GeneratedItem]


@router.post("/generate", response_model=GenerateResponse)
def generate_new_topics(
    body: RecommendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate NEW topics for the student's interests (not taken from the corpus).

    Every generated idea is checked against the corpus and approved titles and dropped
    if it is too similar, then scored for novelty and feasibility.
    """
    if not body.interests.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Describe your interests first.")
    if body.time_budget_weeks <= 0 or body.team_size <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="time_budget_weeks and team_size must be > 0")

    source, items, reason = generate_topics(body, _index, _get_approved_titles(db), n=5)
    notice = (
        "Generated by an AI language model, then checked to be different from all existing projects."
        if source == "llm" else
        f"Offline mode ({reason}): ideas are template-based remixes of nearby domains."
    )
    return GenerateResponse(source=source, notice=notice, recommendations=items)
