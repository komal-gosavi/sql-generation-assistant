import pytest

from app.utils.query_guard import (
    QueryIntentError,
    validate_query_intent,
)


@pytest.mark.parametrize(
    "question",
    [
        "Delete all customers",
        "Update all customer cities",
        "Drop the customers table",
        "Insert a new customer",
        "Truncate the orders table",
        "Alter the customers table",
    ],
)
def test_write_intent_is_blocked(question):
    with pytest.raises(QueryIntentError):
        validate_query_intent(question)


@pytest.mark.parametrize(
    "question",
    [
        "Show all customers",
        "Show customers from Pune",
        "What is the average order value?",
        "Show the top 5 customers by spending",
    ],
)
def test_read_only_questions_are_allowed(question):
    validate_query_intent(question)