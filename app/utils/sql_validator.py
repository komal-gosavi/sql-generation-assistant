import sqlglot
import re
from sqlglot import exp

from app.utils.errors import SQLValidationError


BLOCKED_EXPRESSIONS = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Alter,
    exp.Create,
    exp.Merge,
    exp.Command,
)


def validate_select_only(sql: str) -> str:
    sql = sql.strip()

    if not sql:
        raise SQLValidationError("SQL query cannot be empty.")

    if ";" in sql:
        raise SQLValidationError("Only one SQL statement is allowed.")

    lowered = sql.lower()
    forbidden = [
        "insert", "update", "delete", "drop", "alter", "create",
        "grant", "revoke", "truncate", "merge", "copy", "call", "do"
    ]

    for keyword in forbidden:
        if re.search(rf"\b{re.escape(keyword)}\b", lowered):
            raise SQLValidationError(
                "Only read-only SELECT queries are allowed."
            )

    if not lowered.startswith("select"):
        raise SQLValidationError("Only SELECT statements are allowed.")

    return sql