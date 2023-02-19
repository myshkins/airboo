import pytest
from starlette.testclient import TestClient
from services.api.routers.crud import crud
from services.api.database import get_db
from services.api.main import app


@pytest.fixture
def get_test_db():
    return get_db()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def zipcode():
    return 11206


def test_zipcode_to_latlong(zipcode):
    """
    GIVEN a zipcode
    WHEN zipcode_to_latlong function is called
    THEN a tuple of latitutde longitude coordinates is returned
    """
    coord = crud.zipcode_to_latlong(zipcode)
    assert isinstance(coord, tuple)
    lat, long = coord
    assert -90 <= lat <= 90
    assert -180 <= long <= 180
