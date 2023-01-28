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
        FROM stations_airnow
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
        FROM stations_airnow
        ORDER BY location_coord <-> ':y'::POINT
        LIMIT 1
        """
    )
    result = db.execute(stmt, {'y': loc}).all()
    return result

def get_data(station: str, db: Session):
    stmt = text(
        """
        SELECT             
            station_name,
            reading_datetime,
            pm_10_conc,
            pm_10_AQI,
            pm_10_AQI_CAT,
            pm_25_conc,
            pm_25_AQI,
            pm_25_AQI_CAT
        FROM airnow_readings
        WHERE station_name = :x
        ORDER BY reading_datetime"""
    )
    data = db.execute(stmt, {"x": station}).all()
    return data
