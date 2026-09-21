from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from app.config import GEMINI_API_KEY, MODEL_NAME
from app.utils.errors import LLMServiceError
from app.utils.sql_validator import validate_select_only




llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    max_tokens=900,
    timeout=None,
    max_retries=0,
)


def generate_sql(question: str, database_schema: str) -> str:
    prompt = f"""
You are a PostgreSQL SQL generation assistant.

Your task is to convert the user's natural language question
into one valid PostgreSQL SELECT query.

Database schema:
{database_schema}

User question:
{question}

Rules:
- Generate exactly one SQL statement.
- Generate SELECT statements only.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE,
  CREATE, GRANT, REVOKE, MERGE, or other write/destructive statements.
- Use only tables and columns available in the provided schema.
- Do not invent tables or columns.
- Return only the SQL query.
- Do not use markdown code fences.
- Do not include explanations.
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
    except Exception as exc:
        message = str(exc).lower()
        if "quota" in message or "429" in message or "resource_exhausted" in message:
            raise LLMServiceError("Gemini API quota exceeded. Please try again later.") from exc
        raise LLMServiceError("The SQL generation service is temporarily unavailable.") from exc

    content = response.content

    if isinstance(content, str):
        sql = content.strip()
        return validate_select_only(sql)

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))

        sql = "".join(text_parts).strip()
        return validate_select_only(sql)

    raise TypeError(
        f"Unexpected LLM response content type: {type(content)}"
    )