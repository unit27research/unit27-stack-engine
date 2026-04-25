"""Pydantic schemas for Stack Engine output validation."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, validator


class RecommendedStack(BaseModel):
    intelligence: List[str] = Field(..., min_length=1)
    memory: List[str] = Field(..., min_length=1)
    orchestration: List[str] = Field(..., min_length=1)
    execution: List[str] = Field(..., min_length=1)
    human_approval: List[str] = Field(..., min_length=1)

    @validator("intelligence", "memory", "orchestration", "execution", "human_approval")
    def no_blank_stack_items(cls, value: List[str]) -> List[str]:
        if any(not item.strip() for item in value):
            raise ValueError("Stack categories cannot contain blank tool names.")
        return value


class Workflow(BaseModel):
    name: str = Field(..., min_length=3)
    trigger: str = Field(..., min_length=10)
    steps: List[str] = Field(..., min_length=2)
    human_check: str = Field(..., min_length=10)

    @validator("steps")
    def meaningful_steps(cls, value: List[str]) -> List[str]:
        if any(len(step.strip()) < 10 for step in value):
            raise ValueError("Workflow steps must be specific enough to be useful.")
        return value


class Scorecard(BaseModel):
    impact: int = Field(..., ge=1, le=5)
    reliability: int = Field(..., ge=1, le=5)
    fit: int = Field(..., ge=1, le=5)
    complexity: int = Field(..., ge=1, le=5)
    cost: int = Field(..., ge=1, le=5)
    overall: float | None = None
    verdict: str | None = None


class ScoreRationales(BaseModel):
    impact: str = Field(..., min_length=20)
    reliability: str = Field(..., min_length=20)
    fit: str = Field(..., min_length=20)
    complexity: str = Field(..., min_length=20)
    cost: str = Field(..., min_length=20)


class StackEngineOutput(BaseModel):
    scenario: str = Field(..., min_length=3)
    input_summary: str = Field(..., min_length=20)
    diagnosis: str = Field(..., min_length=40)
    stack: RecommendedStack
    workflows: List[Workflow]
    implementation_steps: List[str]
    scorecard: Scorecard
    score_rationales: ScoreRationales
    verdict: str = Field(..., min_length=8)
    prompts: List[str]

    @validator("verdict")
    def known_verdict(cls, value: str) -> str:
        allowed = {"BUILD NOW", "MANUAL FIRST", "BUILD LATER", "DO NOT BUILD"}
        if value not in allowed:
            raise ValueError(f"Verdict must be one of: {', '.join(sorted(allowed))}.")
        return value

    @validator("workflows")
    def exactly_three_workflows(cls, value: List[Workflow]) -> List[Workflow]:
        if len(value) != 3:
            raise ValueError("Stack Engine output must include exactly 3 workflows.")
        return value

    @validator("implementation_steps")
    def exactly_six_steps(cls, value: List[str]) -> List[str]:
        if len(value) != 6:
            raise ValueError("Stack Engine output must include exactly 6 implementation steps.")
        if any(len(step.strip()) < 20 for step in value):
            raise ValueError("Implementation steps must be specific enough to be useful.")
        return value

    @validator("prompts")
    def exactly_three_prompts(cls, value: List[str]) -> List[str]:
        if len(value) != 3:
            raise ValueError("Stack Engine output must include exactly 3 prompts.")
        if any(len(prompt.strip()) < 20 for prompt in value):
            raise ValueError("Prompts must be specific enough to be useful.")
        return value
