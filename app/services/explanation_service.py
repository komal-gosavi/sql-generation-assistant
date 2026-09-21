from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.utils.errors import LLMServiceError

from app.config import GEMINI_API_KEY, MODEL_NAME



llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    max_tokens=900,
    timeout=None,
    max_retries=0,
)


def explain_query(question: str, sql: str) -> str:
    prompt = f"""
Explain the SQL query in exactly one short sentence.

User question:
{question}

SQL:
{sql}

Rules:
- Explain only what the query does.
- Keep the explanation concise and easy to understand.
- Use plain technical language.
- Mention the main table and filtering condition if applicable.
- Do not explain individual columns.
- Do not mention sorting, grouping, joins, or limits unless they are actually used.
- Do not provide bullet points.
- Do not provide multiple sentences.
- Do not generate or modify SQL.
- Return only the explanation text.
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
        return content.strip()

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))

        return "".join(text_parts).strip()

    raise TypeError(f"Unexpected LLM response content type: {type(content)}")