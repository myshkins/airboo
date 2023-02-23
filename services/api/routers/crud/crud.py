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
        stmt = select(ReadingsAirnow).where(ReadingsAirnow.station_id == id).order_by(ReadingsAirnow.reading_datetime)
        result = db.execute(stmt)
        data = [thing for thing in result]
        response.append(data)
    return response


# def get_data(ids: list[str], db: Session):
#     stmt = text(
#         """
#         SELECT
#             station_id,
#             reading_datetime,
#             pm25_conc,
#             pm25_aqi,
#             pm25_cat,
#             pm10_conc,
#             pm10_aqi,
#             pm10_cat,
#             o3_conc,
#             o3_aqi,
#             o3_cat,
#             co_conc,
#             no2_conc,
#             no2_aqi,
#             no2_cat,
#             so2_conc,
#             so2_aqi,
#             so2_cat
#         FROM readings_airnow
#         WHERE station_id = :x
#         ORDER BY reading_datetime
#         """
#     )
#     result = []
#     for id in ids:
#         data = db.execute(stmt, {"x": id}).all()
#         result.append({"station_id": id, "data": data})
#     return result
