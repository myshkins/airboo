"""api data routes"""

from datetime import datetime as dt

import pgeocode
from fastapi import APIRouter, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


router = APIRouter()

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@postgres/airnow",
    future=True
    )

def zipcode_to_latlong(zipcode: str):
    """helper func, returns tuple of lat long"""
    geo = pgeocode.Nominatim('us')
    loc = geo.query_postal_code(zipcode)
    return float(loc["latitude"]), float(loc["longitude"])

@router.get("/nearest-stations/")
def get_nearest_stations(zipcode: str):
    """with zipcode as query param, returns the nearest station"""
    loc = zipcode_to_latlong(zipcode)
    with engine.connect() as conn:
        stmt = text(
            """
            SELECT station_name, location_coord
            FROM prod_airnow_stations
            ORDER BY location_coord <-> ':y'::POINT
            LIMIT 5
            """
        )
        result = conn.execute(stmt, {"y": loc})
        response = result.all()
        return response

@router.get("/first-station")
def get_first_station(zipcode: str):
    """returns first closest station"""
    stations = get_nearest_stations(zipcode)
    closest = stations[0]
    return closest
