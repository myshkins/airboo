from sqlalchemy import Column, Numeric, String, Integer
from geoalchemy2 import Geometry
from . import Base


class AirnowStationsCommon(Base):
    __abstract__ = True

    station_id = Column(Integer, primary_key=True, nullable=False)
    station_name = Column(String, nullable=False)
    agency_name = Column(String, nullable=False)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    location_coord = Column(Geometry(geometry_type='POINT'), nullable=False)


class AirnowStations(AirnowStationsCommon):
    __tablename__ = 'airnow_stations'


class AirnowStationsTemp(AirnowStationsCommon):
    __tablename__ = 'airnow_stations_temp'