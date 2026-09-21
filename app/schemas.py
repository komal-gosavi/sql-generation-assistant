from typing import Any

from pydantic import BaseModel, Field


class SQLRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class SQLResponse(BaseModel):
    question: str
    sql: str
    results: list[dict[str, Any]]
    explanation: str