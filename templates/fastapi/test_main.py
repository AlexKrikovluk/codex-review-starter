"""Tests for FastAPI application."""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_read_item() -> None:
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}
