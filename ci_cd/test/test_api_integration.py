import pytest
import requests


ZIPCODES = ["11206", 80304, "01913", 99723, "96712"]
ZIPCODES_INVALID = ["Brooklyn, NY", 112060, "11206-1839", "00000", "-----"]


def test_health_check():
    """
    GIVEN   containers are running
    WHEN    health check endpoint is called with GET method
    THEN    response with status 200 and body OK is returned
    """
    response = requests.get("http://air_api:8100/health-check")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


@pytest.mark.parametrize("zipcode", ZIPCODES)
def test_pos_get_nearby_stations(zipcode):
    """
    GIVEN   valid zipcode argument
    WHEN    get_nearby_stations endpoint is called
    THEN    response status is 200 and 
            response body is a list of five stations that conform to the StationsAirnowPydantic model
    """
    response = requests.get(f'http://air_api:8100/stations/all-nearby/?zipcode={zipcode}')
    assert response.status_code == 200
    station_list = response.json()
    assert len(station_list) == 5
    assert all(station_list)


@pytest.mark.parametrize("zipcode", ZIPCODES_INVALID)
def test_neg_get_nearby_stations(zipcode):
    """
    GIVEN   an invalid zipcode argument
    WHEN    get_nearby_stations endpoint is called
    THEN    response body is 400 and response body is error message
    """
    response = requests.get(f'http://air_api:8100/stations/all-nearby/?zipcode={zipcode}')
    assert response.status_code == 400
    assert response.json() == {"detail": "invalid zipcode"}


@pytest.fixture
def station_ids():
    return ["840360470118", "840360610134", "840360810120"]


def test_pos_get_readings_from_ids(station_ids):
    """
    GIVEN   valid station id arguments & valid time period argument
    WHEN    get_readings_from_ids endpoint is called
    THEN    response status is 200 and
            response body is list of readings conforming to ReadingsAirnowPydantic model
            and length of list corresponds to the time period argument passed
    """
    id_lst = [f'?ids={id}&' for id in station_ids]
    query = "".join(id_lst).removesuffix('&')
    response = requests.get(f'http://air_api:8100/air-readings/from-ids/{query}')
    assert response.status_code == 200
