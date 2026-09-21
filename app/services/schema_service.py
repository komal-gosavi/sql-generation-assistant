from sqlalchemy import text
from sqlalchemy.orm import Session


SCHEMA_QUERY = text(
    """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position
    """
)


def get_database_schema(db: Session) -> str:
    rows = db.execute(SCHEMA_QUERY).fetchall()

    schema = {}

    for table_name, column_name, data_type in rows:
        schema.setdefault(table_name, []).append(
            f"{column_name} ({data_type})"
        )

    return "\n".join(
        f"{table}:\n  " + "\n  ".join(columns)
        for table, columns in schema.items()
    )