"""crud functions"""
import pgeocode
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from shared_models.readings_airnow import ReadingsAirnow


def zipcode_to_latlong(zipcode: str):
    """helper func returns tuple of lat long"""
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
