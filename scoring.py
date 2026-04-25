"""Deterministic scoring for Stack Engine recommendations."""

from __future__ import annotations


WEIGHTS = {
    "impact": 0.35,
    "reliability": 0.25,
    "fit": 0.25,
    "complexity": -0.10,
    "cost": -0.05,
}


def calculate_score(
    impact: int,
    reliability: int,
    fit: int,
    complexity: int,
    cost: int,
) -> float:
    """Return the weighted build score rounded to two decimals."""
    raw_score = (
        impact * WEIGHTS["impact"]
        + reliability * WEIGHTS["reliability"]
        + fit * WEIGHTS["fit"]
        + complexity * WEIGHTS["complexity"]
        + cost * WEIGHTS["cost"]
    )
    return round(raw_score, 2)


def verdict_for_score(score: float) -> str:
    """Map deterministic score to a build verdict."""
    if score >= 3.50:
        return "BUILD NOW"
    if score >= 2.75:
        return "MANUAL FIRST"
    if score >= 2.00:
        return "BUILD LATER"
    return "DO NOT BUILD"


def score_payload(scorecard: dict) -> dict:
    """Add score and verdict to an input scorecard dictionary."""
    scored = dict(scorecard)
    overall = calculate_score(
        impact=scored["impact"],
        reliability=scored["reliability"],
        fit=scored["fit"],
        complexity=scored["complexity"],
        cost=scored["cost"],
    )
    scored["overall"] = overall
    scored["verdict"] = verdict_for_score(overall)
    return scored
