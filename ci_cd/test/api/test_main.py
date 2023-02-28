import pytest
import requests
from services.api.main import app


def test_health_check():
    """
    GIVEN containers are running
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = requests.get("localhost:8100/health-check")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}
