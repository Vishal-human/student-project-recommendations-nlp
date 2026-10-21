"""
N1 — Data Schema
ProjectEntry: the typed contract for a single historical project corpus row.
Field names are LOCKED per 08-DATA-AND-API-CONTRACTS.md §1. Do not rename.
"""
from pydantic import BaseModel


class ProjectEntry(BaseModel):
    id: str                      # stable unique id, e.g. "gls-2023-041"
    title: str
    abstract: str                # 1-3 sentence summary; if unavailable, repeat title
    year: int
    department: str              # e.g. "IMCA"
    tech_stack_tags: list[str]   # must come from TAG_LIST in tags.py, lowercase
    domain_tags: list[str]       # lowercase, e.g. ["healthcare", "nlp"]
    language: str = "en"         # ISO 639-1 default "en", not used for matching in v1
