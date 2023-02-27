import pytest
from starlette.testclient import TestClient
import os

from services.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def set_env(monkeypatch):
    monkeypatch.setenv("POSTGRES_URI", "postgresql://airflow:airflow@postgres:5432/air_quality")


def test_env(set_env):
    assert os.environ["DEV_MODE"] == "true"


def test_health_check(client):
    """
    GIVEN the app has started up
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/health-check/")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}
