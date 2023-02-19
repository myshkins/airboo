"""crud functions"""
import pgeocode
from sqlalchemy import text
from sqlalchemy.orm import Session


def zipcode_to_latlong(zipcode: str):
    """helper function, returns tuple of lat long"""
    geo = pgeocode.Nominatim("us")
    loc = geo.query_postal_code(zipcode)
    return loc["latitude"], loc["longitude"]


def get_nearby_stations(zipcode: str, db: Session):
    """given zipcode, returns the 5 nearest stations"""
    loc = zipcode_to_latlong(zipcode)
    stmt = text(
        """
        SELECT station_id, station_name, latitude, longitude, location_coord
        FROM stations_airnow
        ORDER BY location_coord <-> 'SRID=4326;POINT(:y :x)'::geometry
        LIMIT 5
        """
    )
    result = db.execute(stmt, {"x": loc[0], "y": loc[1]}).all()
    return result


def get_closest_station(zipcode: str, db: Session):
    """given zipcode, returns the closest station. note srid=4326 signifies
    that the data is of the latitude/longitude type."""
    loc = zipcode_to_latlong(zipcode)
    stmt = text(
        """
        SELECT station_id, station_name, latitude, longitude, location_coord
        FROM stations_airnow
        ORDER BY location_coord <-> 'SRID=4326;POINT(:y :x)'::geometry
        LIMIT 1
        """
    )
    result = db.execute(stmt, {"x": loc[0], "y": loc[1]}).all()
    return result


def get_data(ids: list[str], db: Session):
    stmt = text(
        """
        SELECT
            station_id,
            reading_datetime,
            pm_25
        FROM readings_waqi
        WHERE station_id = :x
        ORDER BY reading_datetime"""
    )
    result = []
    for id in ids:
        data = db.execute(stmt, {"x": id}).all()
        result.append({"station_id": id, "data": data})
    return result
