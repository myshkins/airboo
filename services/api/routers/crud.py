"""crud functions"""
import pgeocode
from sqlalchemy import text
from sqlalchemy.orm import Session


def zipcode_to_latlong(zipcode: str):
    """helper func, returns tuple of lat long"""
    geo = pgeocode.Nominatim('us')
    loc = geo.query_postal_code(zipcode)
    return loc["latitude"], loc["longitude"]

def get_nearby_stations(zipcode: str, db: Session):
    """given zipcode, returns the 5 nearest stations"""
    loc = zipcode_to_latlong(zipcode)
    stmt = text(
        """
        SELECT station_name, location_coord
        FROM prod_airnow_stations
        ORDER BY location_coord <-> ':y'::POINT
        LIMIT 5
        """
    )
    result = db.execute(stmt, {'y': loc}).all()
    return result

def get_closest_station(zipcode: str, db: Session):
    """given zipcode, returns the closest station"""
    loc = zipcode_to_latlong(zipcode)
    stmt = text(
        """
        SELECT station_name, location_coord
        FROM prod_airnow_stations
        ORDER BY location_coord <-> ':y'::POINT
        LIMIT 1
        """
    )
    result = db.execute(stmt, {'y': loc}).all()
    return result

def get_data(station: str, db: Session):
    stmt = text(
        """
        SELECT * FROM prod_airnow_data
        WHERE station_name = :x
        ORDER BY reading_datetime"""
    )
    data = db.execute(stmt, {"x": station}).all()
    return data
