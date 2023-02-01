from sqlalchemy import Column, Numeric, String
from geoalchemy2 import Geometry
from . import Base


class Airnow_Stations(Base):
    __tablename__ = 'stations_airnow'

    station_name = Column(String, primary_key=True, nullable=False)
    agency_name = Column(String, nullable=False)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    location_coord = Column(Geometry(geometry_type='POINT'), nullable=False)