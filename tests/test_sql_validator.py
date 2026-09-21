import pytest

from app.utils.sql_validator import (
    SQLValidationError,
    validate_select_only,
)


def test_select_query_is_allowed():
    sql = validate_select_only(
        "SELECT * FROM customers"
    )

    assert sql.upper().startswith("SELECT")


@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO customers (name) VALUES ('Test')",
        "UPDATE customers SET city = 'Mumbai'",
        "DELETE FROM customers",
        "DROP TABLE customers",
        "ALTER TABLE customers ADD COLUMN test TEXT",
        "TRUNCATE TABLE customers",
    ],
)
def test_destructive_queries_are_blocked(sql):
    with pytest.raises(SQLValidationError):
        validate_select_only(sql)


def test_multiple_statements_are_blocked():
    with pytest.raises(SQLValidationError):
        validate_select_only(
            "SELECT * FROM customers; DELETE FROM customers"
        )


def test_select_followed_by_drop_is_blocked():
    with pytest.raises(SQLValidationError):
        validate_select_only(
            "SELECT * FROM customers; DROP TABLE customers"
        )