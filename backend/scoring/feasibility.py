"""
N4 — Feasibility Scoring Engine
Pure rule-based, zero ML/network calls. All rules live in rules.yaml.
Exposes exactly one public function per 08-DATA-AND-API-CONTRACTS.md §3.
"""
from __future__ import annotations

from pathlib import Path
import yaml
from pydantic import BaseModel

_RULES_PATH = Path(__file__).parent / "rules.yaml"
_rules: dict = {}


def _load_rules() -> dict:
    global _rules
    if not _rules:
        _rules = yaml.safe_load(_RULES_PATH.read_text(encoding="utf-8"))
    return _rules


class FeasibilityResult(BaseModel):
    score: int              # 0-100 integer
    reasons: list[str]      # human-readable, at least 1 item
    missing_skills: list[str]  # subset of TAG_LIST, may be empty


def score_feasibility(
    student_stack: list[str],
    time_budget_weeks: int,
    team_size: int,
    topic_tags: list[str],
    complexity_tier: str,  # one of "beginner" | "intermediate" | "advanced"
) -> FeasibilityResult:
    """Compute a 0-100 feasibility score with traceable reasons.

    Every deduction has a named reason — no black-box numbers.
    """
    rules = _load_rules()
    student_set = set(s.lower() for s in student_stack)
    score = 100
    reasons: list[str] = []
    missing_skills: list[str] = []

    # 1. Missing skill check: for each topic tag, check if its required skills are present
    tech_req = rules.get("tech_requirements", {})
    for tag in topic_tags:
        for required in tech_req.get(tag, []):
            if required not in student_set:
                if required not in missing_skills:
                    missing_skills.append(required)
                    deduction = 15
                    score -= deduction
                    reasons.append(f"Missing skill: {required} (required for {tag})")

    # 2. Complexity vs time budget check
    time_thresh = rules.get("time_thresholds", {})
    complexity_pen = rules.get("complexity_penalty", {})
    if complexity_tier == "intermediate" and time_budget_weeks < time_thresh.get("intermediate", 3):
        pen = complexity_pen.get("intermediate", 15)
        score -= pen
        reasons.append(
            f"Tight timeline: intermediate topic with only {time_budget_weeks}w budget "
            f"(recommended >= {time_thresh['intermediate']}w)"
        )
    elif complexity_tier == "advanced" and time_budget_weeks < time_thresh.get("advanced", 6):
        pen = complexity_pen.get("advanced", 30)
        score -= pen
        reasons.append(
            f"Tight timeline: advanced topic with only {time_budget_weeks}w budget "
            f"(recommended >= {time_thresh['advanced']}w)"
        )

    # 3. Team size check
    team_min = rules.get("team_size_min", {})
    team_pen = rules.get("team_size_penalty", 10)
    required_team = team_min.get(complexity_tier, 1)
    if team_size < required_team:
        score -= team_pen
        reasons.append(
            f"Small team: {complexity_tier} topics work better with >={required_team} people "
            f"(you have {team_size})"
        )

    # Always include at least one positive reason if nothing is wrong
    if not reasons:
        reasons.append("Good fit: your stack and timeline match this topic well.")

    score = max(0, min(100, score))
    return FeasibilityResult(score=score, reasons=reasons, missing_skills=missing_skills)
