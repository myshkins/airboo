import pytest
from starlette.testclient import TestClient

from services.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    """
    GIVEN the app has started up
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/health-check/")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}
