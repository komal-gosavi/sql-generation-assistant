from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.utils.errors import SQLExecutionError
from app.utils.sql_validator import validate_select_only




def execute_query(db: Session, sql: str) -> list[dict]:
    validated_sql = validate_select_only(sql)
    MAX_ROWS = 1000

    # Ensure a safety limit is applied before sending the query to the DB
    if "limit" not in validated_sql.lower():
        validated_sql = f"{validated_sql.rstrip(';')} LIMIT {MAX_ROWS}"

    try:
        result = db.execute(text(validated_sql))
        rows = [dict(row._mapping) for row in result]

        return rows

    except SQLAlchemyError as exc:
        raise SQLExecutionError(
            "The SQL query could not be executed."
        ) from exc