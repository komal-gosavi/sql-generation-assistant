from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, test_connection
from app.schemas import SQLRequest, SQLResponse
from app.services.explanation_service import explain_query
from app.services.llm_service import generate_sql
from app.services.schema_service import get_database_schema
from app.services.sql_service import execute_query
from app.utils.query_guard import validate_query_intent

from app.utils.errors import (
    LLMServiceError,
    QueryIntentError,
    SQLExecutionError,
    SQLValidationError,
)


app = FastAPI(
    title="SQL Generation Assistant",
    description="Natural language to PostgreSQL SQL assistant",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    try:
        test_connection()
        return {"status": "ok", "database": "connected"}

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable.",
        )


@app.get("/schema")
def database_schema(db: Session = Depends(get_db)):
    return {
        "schema": get_database_schema(db)
    }


@app.post("/generate-sql", response_model=SQLResponse)
def generate_sql_endpoint(
    request: SQLRequest,
    db: Session = Depends(get_db),
):
    try:
        validate_query_intent(request.question)

        schema = get_database_schema(db)

        sql = generate_sql(
            question=request.question,
            database_schema=schema,
        )

        results = execute_query(db, sql)

        explanation = explain_query(
            question=request.question,
            sql=sql,
        )

        return SQLResponse(
            question=request.question,
            sql=sql,
            results=results,
            explanation=explanation,
        )

    except QueryIntentError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except SQLValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except SQLExecutionError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except LLMServiceError as exc:
        message = str(exc)

        if "quota" in message.lower():
            raise HTTPException(
                status_code=429,
                detail=message,
            ) from exc

        raise HTTPException(
            status_code=503,
            detail=message,
        ) from exc

    except Exception as exc:
        print(f"Unexpected error: {type(exc).__name__}: {exc}")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred.",
        ) from exc