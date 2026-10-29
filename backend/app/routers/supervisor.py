"""
Supervisor router — duplicate detection across submitted project topics and
dynamic dataset file ingestion (CSV, TXT, PDF, DOCX) to update corpus and database.
"""
import json
import sys
from collections import Counter
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import CorpusProject, User
from app.deps import require_roles

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

import faiss
import numpy as np

from data.ingest import ingest_file, preprocess_records
from data.loader import load_corpus
from data.schema import ProjectEntry
from ml.index import _embed

router = APIRouter(prefix="/supervisor", tags=["supervisor"])

DUPLICATE_THRESHOLD = 0.75  # cosine similarity above this = flag as likely duplicate
_CORPUS_PATH = _BACKEND_ROOT / "data" / "sample_corpus.json"


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


class CorpusItemPreview(BaseModel):
    id: str
    title: str
    abstract: str
    year: int
    department: str
    tech_stack_tags: list[str]
    domain_tags: list[str]


class CorpusUploadResponse(BaseModel):
    message: str
    filename: str
    total_parsed: int
    added_count: int
    duplicate_count: int
    total_corpus_count: int
    added_entries: list[CorpusItemPreview]


# ---------------------------------------------------------------------------
# Duplicate Detection
# ---------------------------------------------------------------------------

@router.post("/check-duplicates", response_model=DuplicateCheckResponse)
def check_duplicates(
    topics: list[SubmittedTopic],
    current_user: User = Depends(require_roles("teacher", "supervisor")),
):
    """Detect near-duplicate project topics across all submitted topics."""
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


# ---------------------------------------------------------------------------
# Corpus Upload & Dataset Management
# ---------------------------------------------------------------------------

@router.post("/corpus/upload", response_model=CorpusUploadResponse)
async def upload_corpus_data_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("teacher", "supervisor")),
):
    """Upload data file (.csv, .txt, .pdf, .docx, .json) to expand the historical corpus.

    1. Parses file format & extracts records.
    2. Cleans text, auto-tags tech stack & domains, and maps to ProjectEntry schema.
    3. Deduplicates against existing corpus.
    4. Updates backend/data/sample_corpus.json.
    5. Saves new records to corpus_projects DB table.
    6. Hot-reloads the FAISS index so new projects are immediately available for recommendations.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        raw_records = ingest_file(file.filename, content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(exc)}")

    if not raw_records:
        raise HTTPException(
            status_code=400,
            detail="No valid project records or titles could be extracted from this file."
        )

    # Load existing corpus
    existing_entries = load_corpus(str(_CORPUS_PATH))
    new_entries, duplicate_count = preprocess_records(raw_records, existing_entries)

    if new_entries:
        # 1. Update sample_corpus.json
        combined_corpus = existing_entries + new_entries
        corpus_dicts = [e.model_dump() for e in combined_corpus]
        _CORPUS_PATH.write_text(json.dumps(corpus_dicts, indent=2, ensure_ascii=False), encoding="utf-8")

        # 2. Update DB table
        for e in new_entries:
            db_item = CorpusProject(
                id=e.id,
                title=e.title,
                abstract=e.abstract,
                year=e.year,
                department=e.department,
                tech_stack_tags=json.dumps(e.tech_stack_tags),
                domain_tags=json.dumps(e.domain_tags),
                source="upload",
            )
            db.merge(db_item)
        db.commit()

        # 3. Hot-reload FAISS index in topics router
        from app.routers.topics import reload_corpus_and_index
        total_count = reload_corpus_and_index()
    else:
        total_count = len(existing_entries)

    previews = [
        CorpusItemPreview(
            id=e.id,
            title=e.title,
            abstract=e.abstract,
            year=e.year,
            department=e.department,
            tech_stack_tags=e.tech_stack_tags,
            domain_tags=e.domain_tags,
        )
        for e in new_entries[:10]
    ]

    return CorpusUploadResponse(
        message=f"Successfully processed '{file.filename}'. Added {len(new_entries)} new projects.",
        filename=file.filename,
        total_parsed=len(raw_records),
        added_count=len(new_entries),
        duplicate_count=duplicate_count,
        total_corpus_count=total_count,
        added_entries=previews,
    )


@router.get("/corpus/stats")
def get_corpus_stats(
    current_user: User = Depends(require_roles("teacher", "supervisor")),
):
    """Return overview metrics and domain distribution for the active corpus."""
    entries = load_corpus(str(_CORPUS_PATH))
    domain_counts = Counter()
    for e in entries:
        for d in e.domain_tags:
            domain_counts[d] += 1

    year_counts = Counter(e.year for e in entries)

    return {
        "total_projects": len(entries),
        "domain_distribution": dict(sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)),
        "year_distribution": dict(sorted(year_counts.items(), reverse=True)),
        "recent_sample": [
            {
                "id": e.id,
                "title": e.title,
                "domain_tags": e.domain_tags,
                "tech_stack_tags": e.tech_stack_tags,
                "year": e.year,
            }
            for e in entries[-6:]
        ],
    }
