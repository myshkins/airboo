import pytest
import requests


ZIPCODES = ["11205", 80304, "01913", 99723, "96712"]


def test_health_check():
    """
    GIVEN containers are running
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = requests.get("http://air_api:8100/health-check")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


@pytest.mark.parametrize("zipcode", ZIPCODES)
def test_get_nearby_stations(zipcode):
    """
    GIVEN a list of valid zipcodes
    WHEN each zipcode is given as argument to get_nearby_stations endpoint call
    THEN response body is a list of stations that conform to the Station pydantic model"""
    response = requests.get(f'http://air_api:8100/stations/all-nearby/?zipcode={zipcode}')
    assert response.status_code == 200
    station_list = response.json()
    assert len(station_list) == 5
    assert all(station_list)
