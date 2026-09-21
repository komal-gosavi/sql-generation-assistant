class AppError(Exception):
    """Base exception for application errors."""


class QueryIntentError(AppError):
    """Raised when the user requests a write/destructive operation."""


class SQLValidationError(AppError):
    """Raised when generated SQL is invalid or unsafe."""


class SQLExecutionError(AppError):
    """Raised when SQL execution fails."""


class LLMServiceError(AppError):
    """Raised when the LLM service fails."""