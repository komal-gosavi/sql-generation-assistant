# SQL Generation Assistant

> Natural language → safe, read-only PostgreSQL SQL using Gemini.

## Overview

SQL Generation Assistant converts natural-language questions into PostgreSQL `SELECT` queries. It reads the live database schema, validates generated SQL, executes it using a read-only database user, and returns results with a short explanation.

The project is designed with multiple safety layers to prevent destructive SQL operations.

## Key Features

- Natural language → PostgreSQL SQL generation
- Live database schema awareness
- `SELECT`-only SQL validation with SQLGlot
- Natural-language write-operation guard
- Read-only PostgreSQL user
- SQL execution with SQLAlchemy
- Query explanation using Gemini
- FastAPI REST API with Swagger UI
- Centralized error handling
- Dockerized PostgreSQL
- Automated tests with pytest

## Tech Stack

- **Python 3.11+**
- **FastAPI** — API framework
- **PostgreSQL** — database
- **SQLAlchemy** — database access
- **SQLGlot** — SQL parsing and validation
- **LangChain** — LLM integration
- **Google Gemini** — SQL generation and explanation
- **Pydantic** — request/response validation
- **Docker Compose** — PostgreSQL environment
- **pytest** — testing
- **uv** — Python package management

## Prerequisites

- Python 3.11+
- Docker Desktop
- A Gemini API key
- uv

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd sql-generation-assistant
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+psycopg://sql_assistant_app:readonly_password@localhost:5432/sql_assistant
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

### 5. Run the API

```bash
uv run uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Usage

Send a request to `/generate-sql`:

```json
{
  "question": "Show the top 5 customers by total spending."
}
```

The API returns the generated SQL, query results, and a short explanation.

**Example read-only questions:**

```text
Show all customers from Pune.
What is the average order value?
Show the top 5 customers by total spending.
List the 5 most expensive products.
```

**Write or destructive requests are rejected**, for example:

```text
Delete all customers.
Update customer cities.
Drop the customers table.
```

## Project Structure

```text
sql-generation-assistant/
├── app/
│   ├── services/
│   └── utils/
├── database/
├── tests/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── sample_queries.md
```

- [`app/services/`](app/services/) — schema extraction, SQL generation, execution, and query explanation.
- [`app/utils/`](app/utils/) — query guards, SQL validation, and application errors.
- [`database/`](database/) — PostgreSQL initialization and read-only user setup.
- [`tests/`](tests/) — automated tests.
- [`sample_queries.md`](sample_queries.md) — example supported and blocked questions.

## Architecture

```text
User
  │
  ▼
FastAPI API
  │
  ├── Query Intent Guard
  │
  ├── Database Schema
  │
  ▼
Gemini LLM
  │
  ▼
SQLGlot Validator
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
(Read-Only User)
  │
  ▼
Results + Explanation
  │
  ▼
API Response
```

## Techniques

### Schema-aware generation

The application reads PostgreSQL `information_schema` and provides the current table and column information to Gemini before generating SQL.

### AST-based SQL validation

SQLGlot parses generated SQL into an abstract syntax tree (AST). The application accepts one `SELECT` statement and rejects destructive operations.

### Defense in depth

Safety is enforced at multiple levels:

```text
User question
     ↓
Query intent guard
     ↓
Gemini SQL generation
     ↓
SQLGlot validation
     ↓
Read-only PostgreSQL permissions
     ↓
Query execution
```

### Structured HTTP errors

Application errors are mapped to HTTP responses so API clients receive clear failure messages. See [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status).

### Environment-based configuration

API keys and database credentials are loaded from environment variables instead of being hard-coded.

## Roadmap

Possible future improvements:

- Add authentication and rate limiting
- Add more database dialects
- Improve query explanation and error messages
- Add CI checks and coverage reporting
- Add a lightweight web interface

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add tests.
4. Run the test suite:

```bash
uv run pytest
```

5. Open a pull request with a clear description of the change.
