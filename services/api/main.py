"""api routes"""
from fastapi import FastAPI
import pgeocode
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/airnow")

metadata_obj = MetaData()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello myshy"}

def zipcode_to_latlong(zipcode: str):
    """helper func, returns tuple of lat long"""
    geo = pgeocode.Nominatim('us')
    loc = geo.query_postal_code(zipcode)
    return float(loc["latitude"]), float(loc["longitude"])

@app.get("/nearest-station/{zipcode}")
def get_nearest_station(zipcode: str):
    """with zipcode as arg, returns the nearest station"""
    loc = zipcode_to_latlong(zipcode)
    with Session(engine) as session:
        stmt = text(
            """
            SELECT station_name, location_coord
            FROM airnow_stations
            ORDER BY location_coord <-> ':y'::POINT
            LIMIT 5
            """
        )
        result = session.execute(stmt, {"y": loc})
        response = [row for row in result]
        return response

