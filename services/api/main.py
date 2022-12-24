"""api routes"""
from datetime import timedelta, datetime as dt
from fastapi import FastAPI
import pgeocode
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/airnow", future=True)

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
            FROM airnow_stations
            ORDER BY location_coord <-> ':y'::POINT
            LIMIT 5
            """
        )
        result = conn.execute(stmt, {"y": loc})
        response = result.all()
        return response

@app.get("/air-data-near-me/")
def get_air_data_near_me(period: str, zipcode: str):
    stations = get_nearest_station(zipcode)
    if period not in ["day", "week", "month"]:
        return "Error, please select a time frame of either 'day', 'week, or" \
               "'month"
    if period == "day":
        q_period = timedelta(hours=24)
    if period == "week":
        q_period = timedelta(days=7)
    if period == "month":
        q_period = timedelta(days=30)
    now = dt.now()
    with engine.connect() as conn:
        stmt = text(
            """
            SELECT * FROM airnow_readings
            ORDER BY reading_datetime"""
        )
        result = conn.execute(stmt)
        data = result.all()
        return data
