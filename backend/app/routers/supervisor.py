"""
Supervisor router — duplicate detection across submitted project topics.
This is the B2B wedge: the tool supervisors/HODs actually pay for.

POST /supervisor/check-duplicates
  Accepts a list of submitted project topics and returns pairs
  with high semantic similarity (potential duplicates).
"""
import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.db.models import User
from app.deps import require_roles

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from ml.index import _embed
import numpy as np
import faiss

router = APIRouter(prefix="/supervisor", tags=["supervisor"])

DUPLICATE_THRESHOLD = 0.75  # cosine similarity above this = flag as likely duplicate


class SubmittedTopic(BaseModel):
    student_name: str
    roll_no: str
    title: str
    abstract: str = ""


class DuplicatePair(BaseModel):
    student_a: str
    roll_a: str
    title_a: str
    student_b: str
    roll_b: str
    title_b: str
    similarity_pct: int
    risk_level: str  # "HIGH" | "MEDIUM"


class DuplicateCheckResponse(BaseModel):
    total_submissions: int
    flagged_pairs: list[DuplicatePair]
    clean_topics: int


@router.post("/check-duplicates", response_model=DuplicateCheckResponse)
def check_duplicates(
    topics: list[SubmittedTopic],
    current_user: User = Depends(require_roles("teacher", "supervisor")),
):
    """Detect near-duplicate project topics across all submitted topics.

    Uses semantic similarity (sentence embeddings) — not just string matching.
    This catches paraphrased duplicates that manual spreadsheet review misses.
    """
    if len(topics) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 topics to compare.")

    texts = [f"{t.title}. {t.abstract}" if t.abstract else t.title for t in topics]
    vecs = _embed(texts)

    dim = vecs.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vecs)

    flagged: list[DuplicatePair] = []
    seen = set()

    for i, vec in enumerate(vecs):
        distances, indices = index.search(vec.reshape(1, -1), k=len(topics))
        for dist, j in zip(distances[0], indices[0]):
            if j == i or j == -1:
                continue
            pair_key = tuple(sorted([i, j]))
            if pair_key in seen:
                continue
            sim = float(np.clip(dist, 0.0, 1.0))
            if sim >= DUPLICATE_THRESHOLD:
                seen.add(pair_key)
                flagged.append(DuplicatePair(
                    student_a=topics[i].student_name,
                    roll_a=topics[i].roll_no,
                    title_a=topics[i].title,
                    student_b=topics[j].student_name,
                    roll_b=topics[j].roll_no,
                    title_b=topics[j].title,
                    similarity_pct=int(sim * 100),
                    risk_level="HIGH" if sim >= 0.88 else "MEDIUM",
                ))

    flagged.sort(key=lambda p: p.similarity_pct, reverse=True)
    return DuplicateCheckResponse(
        total_submissions=len(topics),
        flagged_pairs=flagged,
        clean_topics=len(topics) - len({p.roll_a for p in flagged} | {p.roll_b for p in flagged}),
    )
