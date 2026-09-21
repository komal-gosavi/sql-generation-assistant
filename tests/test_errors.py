import pytest

from app.utils.errors import (
    LLMServiceError,
    QueryIntentError,
    SQLExecutionError,
    SQLValidationError,
)


def test_query_intent_error():
    with pytest.raises(QueryIntentError):
        raise QueryIntentError("Write operation blocked.")


def test_sql_validation_error():
    with pytest.raises(SQLValidationError):
        raise SQLValidationError("Invalid SQL.")


def test_sql_execution_error():
    with pytest.raises(SQLExecutionError):
        raise SQLExecutionError("SQL execution failed.")


def test_llm_service_error():
    with pytest.raises(LLMServiceError):
        raise LLMServiceError("Gemini unavailable.")