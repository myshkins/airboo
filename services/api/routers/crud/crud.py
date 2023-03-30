"""crud functions"""
from datetime import timedelta, datetime as dt
import math
import pandas as pd
import pgeocode

# from logger import LOGGER
from shared_models.readings_airnow import ReadingsAirnow
from shared_models.pydantic_models import Location, PollutantEnum, TimeEnum
from sqlalchemy import select, text
from sqlalchemy.orm import Session, load_only


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
        SELECT
            station_id,
            station_name,
            agency_name,
            status,
            latitude,
            longitude,
            elevation,
            country
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
        SELECT
            station_id,
            station_name,
            agency_name,
            status,
            latitude,
            longitude,
            elevation,
            country
        FROM stations_airnow
        WHERE station_id IN (select station_id FROM readings_airnow)
        ORDER BY location_coord <-> 'SRID=4326;POINT(:y :x)'::geometry
        LIMIT 1
        """
    )
    result = db.execute(stmt, {"x": loc.lat, "y": loc.long}).all()
    return result


def get_data(
    ids: list[str], db: Session, period: TimeEnum, pollutants: list[PollutantEnum]
) -> list[dict]:
    """returns data for given station_ids, time period, and pollutants"""
    response = []
    with db.connection() as conn:
        for id in ids:
            for pol in pollutants:
                stmt = (
                    select(ReadingsAirnow)
                    .options(load_only(pol.column()))
                    .where(ReadingsAirnow.station_id == id)
                    .where(ReadingsAirnow.reading_datetime > period.start())
                    .order_by(ReadingsAirnow.reading_datetime)
                )
                df = pd.read_sql_query(stmt, conn)
                df = (
                    df.resample(period.letter(), on="reading_datetime")
                    .mean(numeric_only=True)
                    .round(decimals=0)
                    .reset_index()
                    .fillna(value=0)
                )
                if df.empty or len(df.columns) == 1:
                    continue
                j = df.to_dict(orient="records")
                response.append({"station_id": id, "pollutant": pol, "readings": j})
    return response


def get_not_null_pollutants(df: pd.DataFrame) -> list:
    not_null_pollutants = []
    plt_list = ["pm25_aqi", "pm10_aqi", "o3_aqi", "co_aqi", "no2_aqi", "so2_aqi"]
    for col in df.columns:
        if df[col][0] is not None and col in plt_list:
            p = col.removesuffix("_aqi")
            not_null_pollutants.append(p)
    return not_null_pollutants


def get_pollutants(ids: list[str], db: Session) -> list:
    """returns pollutants for given station_ids"""
    response = []
    with db.connection() as conn:
        for id in ids:
            stmt = (
                select(ReadingsAirnow)
                .where(ReadingsAirnow.station_id == id)
                .where(
                    ReadingsAirnow.reading_datetime > (dt.now() - timedelta(hours=2))
                )
                .order_by(ReadingsAirnow.reading_datetime)
            )
            df = pd.read_sql_query(stmt, conn)
            if df.empty or len(df.columns) == 1:
                continue
            not_null_pollutants = get_not_null_pollutants(df)
            response.append({"station_id": id, "pollutants": not_null_pollutants})
    return response
