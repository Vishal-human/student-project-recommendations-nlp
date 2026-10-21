"""
Shared pytest fixtures for the TopicMatch NLP test suite.
The FAISS index is built ONCE per session (slow due to SBERT encoding).
"""
import sys
from pathlib import Path

# Allow imports from backend root
_BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BACKEND))

import pytest
from data.loader import load_corpus
from ml.index import build_index

_CORPUS_PATH = _BACKEND / "data" / "sample_corpus.json"


@pytest.fixture(scope="session")
def corpus():
    """Load the committed corpus (data/sample_corpus.json)."""
    return load_corpus(str(_CORPUS_PATH))


@pytest.fixture(scope="session")
def index(corpus):
    """Build FAISS index once for the whole test session."""
    return build_index(corpus)
