from pydantic import BaseModel, Field
from typing import Literal

import json

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
    line: int = Field(ge=1)

    description: str
    suggestion: str


class ReviewResult(BaseModel):
    issues: list[ReviewIssue]


def parse_llm_response(raw_output: str) -> ReviewResult:
    cleaned = raw_output.strip()

    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    data = json.loads(cleaned)

    return ReviewResult.model_validate(data)