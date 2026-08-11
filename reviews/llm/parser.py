from pydantic import BaseModel, Field, ValidationError
from typing import Literal

import json
import re


class ReviewIssue(BaseModel):
    issue_type: Literal[
        "bug",
        "security",
        "performance",
        "validation",
        "edge_case",
    ]

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ]

    confidence: float = Field(ge=0.0, le=1.0)

    file: str
    line_content: str

    description: str
    suggestion: str


class ReviewResult(BaseModel):
    issues: list[ReviewIssue]


def parse_llm_response(raw_output: str) -> ReviewResult:

    cleaned = raw_output.strip()

    # Remove markdown code fences
    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    cleaned = cleaned.strip()

    # Parse JSON
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid JSON: {exc}"
        ) from exc

    # Validate schema
    try:
        return ReviewResult.model_validate(data)
    except ValidationError as exc:
        raise ValueError(
            f"LLM returned invalid review schema: {exc}"
        ) from exc