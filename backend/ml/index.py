"""
N3 — Embedding + FAISS Vector Index
Exposes exactly two public functions per 08-DATA-AND-API-CONTRACTS.md §2:
  build_index(entries) -> FaissIndexWrapper
  query(index, text, k=5) -> list[MatchResult]

Model is loaded ONCE at module import, not per call.
All embeddings are L2-normalized so IndexFlatIP gives cosine similarity.
"""
from __future__ import annotations

import numpy as np
import faiss
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from data.schema import ProjectEntry

# Model loaded once at module import — never reload per call.
# all-mpnet-base-v2: stronger embeddings than MiniLM, still CPU-runnable (~420MB).
# Key upgrade for startup quality: better semantic discrimination on short project titles.
_MODEL = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


class MatchResult(BaseModel):
    entry: ProjectEntry
    similarity: float  # cosine similarity, range 0.0–1.0 (NOT percentage)


class FaissIndexWrapper:
    """Opaque wrapper: holds the FAISS index + parallel ProjectEntry list."""
    def __init__(self, index: faiss.Index, entries: list[ProjectEntry]) -> None:
        self._index = index
        self._entries = entries


def _embed(texts: list[str]) -> np.ndarray:
    """Embed a list of strings and L2-normalize (enables cosine via IndexFlatIP)."""
    vecs = _MODEL.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    faiss.normalize_L2(vecs)
    return vecs.astype("float32")


def build_index(entries: list[ProjectEntry]) -> FaissIndexWrapper:
    """Embed corpus once and build a FAISS IndexFlatIP for cosine similarity search."""
    texts = [f"{e.title}. {e.abstract}" for e in entries]
    vecs = _embed(texts)
    dim = vecs.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vecs)
    return FaissIndexWrapper(index, entries)


def query(index: FaissIndexWrapper, text: str, k: int = 5) -> list[MatchResult]:
    """Return top-k nearest corpus entries, sorted by descending cosine similarity."""
    vec = _embed([text])
    # Clamp k to number of indexed entries
    k = min(k, index._index.ntotal)
    distances, indices = index._index.search(vec, k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        results.append(MatchResult(
            entry=index._entries[idx],
            similarity=float(np.clip(dist, 0.0, 1.0)),
        ))
    # Already sorted descending by FAISS, but enforce explicitly
    results.sort(key=lambda r: r.similarity, reverse=True)
    return results
