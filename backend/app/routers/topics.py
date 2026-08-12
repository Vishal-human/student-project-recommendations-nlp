import json
from collections import Counter
from pathlib import Path

from fastapi import APIRouter, Depends

from app.db.models import User
from app.deps import get_current_user

router = APIRouter(prefix="/topics", tags=["topics"])

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "topics.json"
with open(DATA_PATH) as f:
    _TOPICS = json.load(f)


@router.get("/domains")
def list_domains(current_user: User = Depends(get_current_user)):
    """Domain names + topic counts from the Stage 2 dataset.

    A preview only — full NLP-based topic matching (Stage 2) isn't wired up yet.
    """
    counts = Counter(topic["domain"] for topic in _TOPICS)
    return {
        "total_topics": len(_TOPICS),
        "domains": [{"domain": domain, "count": count} for domain, count in sorted(counts.items())],
    }
