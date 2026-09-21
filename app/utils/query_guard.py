import re

from app.utils.errors import QueryIntentError


BLOCKED_PATTERNS = [
    r"\b(insert|update|delete|truncate|replace|merge)\b",
    r"\bdrop\s+(?:the\s+)?(?:\w+\s+)?(table|database|schema|column|index|view)\b",
    r"\balter\s+(?:the\s+)?(?:\w+\s+)?(table|database|schema|column|index|view)\b",
    r"\bcreate\s+(table|database|schema|index|view)\b",
    r"\b(remove|erase|destroy)\s+(all|the|customer|customers|order|orders|product|products|data|records)\b",
]


def validate_query_intent(question: str) -> None:
    normalized = question.lower().strip()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, normalized):
            raise QueryIntentError(
                "Only read-only data retrieval questions are allowed."
            )