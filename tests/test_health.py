"""Smoke tests for ADES public surfaces."""

from fastapi.testclient import TestClient
from src.core.orchestration.api import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_version():
    from src import __version__

    assert __version__ == "0.1.0"
