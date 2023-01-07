"""api data routes"""

from datetime import datetime as dt

import pgeocode
from fastapi import APIRouter, FastAPI
from sqlalchemy import create_engine, text


router = APIRouter(
    prefix="/air-data",
    tags=["air-data"],
)

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@postgres/airnow",
    future=True
    )

    
def query_airnow(station):
    with engine.connect() as conn:
        stmt = text(
            """
            SELECT * FROM prod_airnow_data
            WHERE station_name = :x
            ORDER BY reading_datetime"""
        )
        result = conn.execute(stmt, {"x": station})
        data = result.all()
        return data

@router.get("/air-data-near-me/")
def get_air_data_near_me(zipcode: str):
    stations = get_nearest_stations(zipcode)
    
    result = []
    for station in stations:
        s_name = station["station_name"]
        s_data = query_airnow(q_period, s_name)
        result.append(s_data)
    return result

