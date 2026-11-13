import pytest

pytest.importorskip("fastapi")
pytest.importorskip("sqlalchemy")
pytest.importorskip("pydantic_settings")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def test_health_ok():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "test"}


def test_health_db_ok():
    with TestClient(app) as client:
        response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
