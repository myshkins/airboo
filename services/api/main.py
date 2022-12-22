"""api routes"""
from fastapi import FastAPI
import pgeocode
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres/airflow")
Session = sessionmaker(engine)

metadata_obj = MetaData()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello myshy"}

def zipcode_to_latlong(zipcode: str):
    """helper func, returns tuple of lat long"""
    geo = pgeocode.Nominatim('us')
    loc = geo.query_postal_code(zipcode)
    return loc["latitude"], loc["longitude"]

@app.get("/nearest-station/{zipcode}")
def get_nearest_station(zipcode: str):
    """with zipcode as arg, returns the nearest station"""
    loc = zipcode_to_latlong(zipcode)
    with Session.begin() as session:
