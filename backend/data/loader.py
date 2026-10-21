"""
N2 — Corpus Loader
load_corpus(path) -> list[ProjectEntry]
Validates every row strictly — raises ValueError on first invalid row.
"""
import json
from pathlib import Path

from data.schema import ProjectEntry


def load_corpus(path: str) -> list[ProjectEntry]:
    """Load and validate a JSON corpus file.

    Args:
        path: path to a JSON file containing a list of project entry dicts.

    Returns:
        List of validated ProjectEntry objects.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: on the first row that fails schema validation (no silent skipping).
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    entries: list[ProjectEntry] = []
    for i, row in enumerate(data):
        try:
            entries.append(ProjectEntry(**row))
        except Exception as exc:
            raise ValueError(f"Invalid row at index {i}: {exc}") from exc
    return entries
