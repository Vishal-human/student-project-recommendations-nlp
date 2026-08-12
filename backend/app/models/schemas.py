from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TopicOut(BaseModel):
    id: int
    title: str
    description: str
    domain: str
    tags: list[str]
    difficulty: str


class RecommendedTopic(TopicOut):
    score: float
    matched_keywords: list[str] = []


class RecommendRequest(BaseModel):
    interests: str = Field(..., min_length=3, description="Free text describing skills/interests")
    top_k: int = Field(5, ge=1, le=20)
    domain: Optional[str] = None


class RecommendResponse(BaseModel):
    query: str
    results: list[RecommendedTopic]


class ClusterOut(BaseModel):
    cluster_id: int
    topics: list[dict]
