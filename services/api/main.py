"""api routes"""
from enum import Enum

from datetime import timedelta, datetime as dt
from fastapi import FastAPI
import pgeocode
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

class TimePeriod(str, Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@postgres/airnow",
    future=True
    )
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello myshy"}

def zipcode_to_latlong(zipcode: str):
    """helper func, returns tuple of lat long"""
    geo = pgeocode.Nominatim('us')
    loc = geo.query_postal_code(zipcode)
    return float(loc["latitude"]), float(loc["longitude"])

@app.get("/nearest-station/")
def get_nearest_station(zipcode: str):
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

def query_airnow(period, station):
    now = dt.now()
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

@app.get("/air-data-near-me/")
def get_air_data_near_me(period: TimePeriod, zipcode: str):
    stations = get_nearest_station(zipcode)
    nearest_station = stations[0]["station_name"]
    if period is TimePeriod.day:
        q_period = timedelta(hours=24)
    if period is TimePeriod.week:
        q_period = timedelta(days=7)
    if period is TimePeriod.month:
        q_period = timedelta(days=30)
    if period is TimePeriod.year:
        q_period = timedelta(days=365)

    result = []
    for station in stations:
        s_name = station["station_name"]
        s_data = query_airnow(q_period, s_name)
        result.append(s_data)
    return result

