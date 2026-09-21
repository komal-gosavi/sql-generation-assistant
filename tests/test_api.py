from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_schema():
    response = client.get("/schema")

    assert response.status_code == 200
    assert "schema" in response.json()


def test_empty_question():
    response = client.post(
        "/generate-sql",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_write_intent_is_rejected():
    response = client.post(
        "/generate-sql",
        json={"question": "Delete all customers"},
    )

    assert response.status_code == 400