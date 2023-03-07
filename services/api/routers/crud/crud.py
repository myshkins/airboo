"""crud functions"""
import math

import pgeocode
import pandas as pd
from shared_models.pydantic_models import Location, TimePeriod
from shared_models.readings_airnow import ReadingsAirnow
from sqlalchemy import select, text
from sqlalchemy.orm import Session


def zipcode_to_latlong(zipcode: str) -> Location:
    """helper func returns tuple of lat long"""
    geo = pgeocode.Nominatim("us")
    loc = geo.query_postal_code(zipcode)
    if math.isnan(loc["latitude"]):
        return 1
    location = Location(lat=loc["latitude"], long=loc["longitude"])
    return location


def get_nearby_stations(zipcode: str, db: Session) -> list:
    """given zipcode, returns the 5 nearest stations"""
    loc = zipcode_to_latlong(zipcode)
    if loc == 1:
        return 1
    stmt = text(
        """
        SELECT station_id, station_name, agency_name, status, latitude, longitude, elevation, country
        FROM stations_airnow
        WHERE station_id IN (select station_id FROM readings_airnow)
        ORDER BY location_coord <-> 'SRID=4326;POINT(:y :x)'::geometry
        LIMIT 5
        """
    )
    result = db.execute(stmt, {"x": loc.lat, "y": loc.long}).all()
    return result


def get_closest_station(zipcode: str, db: Session):
    """returns closest station to zipcode. note srid=4326 signifies data is of
    the latitude/longitude type."""
    loc = zipcode_to_latlong(zipcode)
    stmt = text(
        """
        SELECT station_id, station_name, agency_name, status, latitude, longitude, elevation, country
        FROM stations_airnow
        WHERE station_id IN (select station_id FROM readings_airnow)
        ORDER BY location_coord <-> 'SRID=4326;POINT(:y :x)'::geometry
        LIMIT 1
        """
    )
    result = db.execute(stmt, {"x": loc.lat, "y": loc.long}).all()
    return result


def get_data(ids: list[str], db: Session) -> list[dict]:
    response = []
    for id in ids:
        stmt = (
            select(
                ReadingsAirnow.reading_datetime,
                ReadingsAirnow.pm25_aqi,
                ReadingsAirnow.pm25_conc,
                ReadingsAirnow.pm25_cat,
                ReadingsAirnow.pm10_aqi,
                ReadingsAirnow.pm10_conc,
                ReadingsAirnow.pm10_cat,
                ReadingsAirnow.o3_aqi,
                ReadingsAirnow.o3_conc,
                ReadingsAirnow.o3_cat,
                ReadingsAirnow.co_conc,
                ReadingsAirnow.no2_aqi,
                ReadingsAirnow.no2_conc,
                ReadingsAirnow.no2_cat,
                ReadingsAirnow.so2_aqi,
                ReadingsAirnow.so2_conc,
                ReadingsAirnow.so2_cat,
            )
            .where(ReadingsAirnow.station_id == id)
            .order_by(ReadingsAirnow.reading_datetime)
        )
        result = db.execute(stmt)
        data = [_ for _ in result]
        response.append({"station_id": id, "readings": data})
    return response


def create_dfs(response: list[dict]):
    dfs = []
    for station in response:
        df = pd.DataFrame.from_records(station["readings"])
        df["reading_datetime"] = pd.to_datetime(df["reading_datetime"])
        dfs.append(df)
    return dfs


def select_for_time_period(response: list[dict], period: TimePeriod) -> list[dict]:
    dfs = create_dfs(response)
