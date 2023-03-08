import pytest
import requests
import sys
import os
from pandas import DataFrame
from sqlalchemy import create_engine

root = os.path.realpath(os.path.dirname(__file__) + "/../..")
api_path = root + "/services/api"

sys.path.append(os.path.realpath(root))
sys.path.append(os.path.realpath(api_path))

from services.api.routers.crud import crud
from services.api.database import get_db
from services.api.config import Settings

ZIPCODES = ["11206", 80304, "01913", 99723, "96712"]
ZIPCODES_INVALID = ["Brooklyn, NY", 112060, "11206-1839", "00000", "-----"]
POSTGRES_URI = os.environ["POSTGRES_URI"]


@pytest.fixture
def station_ids():
    return ["840360470118", "840360610134", "840360810120"]


@pytest.fixture
def invalid_station_ids():
    return ["not and id", "", 0, 1, "0000", 000000000000, "000000000000"]


@pytest.fixture
def engine():
    engine = create_engine(POSTGRES_URI)
    return engine


def test_health_check():
    """
    GIVEN   containers are running
    WHEN    health check endpoint is called with GET method
    THEN    response with status 200 and body OK is returned
    """
    response = requests.get("http://air_api:8100/health-check")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


def test_create_dfs(station_ids, engine):
    """
    GIVEN   a list of valid station ids
    WHEN    create_dfs is called
    THEN    a list of dfs is returned
    """
    with engine.connect() as conn:
        dfs = crud.get_pandas(station_ids, conn)
    assert len(dfs) == 3
    assert all([isinstance(df, DataFrame) for df in dfs])


def test_filter_data_time(ids, period, db):
    """
    given   a list of ids and valid time period argument
    when    filter_data_time is called
    then    the data is filtered for the given time period
    """
    result = crud.filter_data(ids, period, db)
    assert 


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


def test_neg_get_readings_from_ids():
    """
    GIVEN   invalid station id arguments and valid time period argument
    WHEN    get_readings_from_ids enpoint is called
    THEN    response status is 400 and response body is error message
    """
    pass
