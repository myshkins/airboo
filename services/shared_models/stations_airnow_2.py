from geoalchemy2 import Geometry
from sqlalchemy import Column, Numeric, String

from . import Base


class AirnowStations_2(Base):
    __abstract__ = True

    station_id = Column(String, primary_key=True, nullable=False)
    station_name = Column(String, nullable=False)
    agency_name = Column(String, nullable=False)
    status = Column(String, nullable=True)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    elevation = Column(Numeric(10, 6), nullable=True)
    country_fips = Column(String, nullable=True)
    location_coord = Column(Geometry(geometry_type='POINT'), nullable=True)


class AirnowStationsTemp_2(Base):
    __tablename__ = 'stations_airnow_temp_2'

    station_id = Column(String, nullable=True)
    aqsid = Column(String, nullable=True)
    full_aqsid = Column(String, nullable=True)
    parameter = Column(String, nullable=True)
    monitor_type = Column(String, nullable=True)
    site_code = Column(String, nullable=True)
    site_name = Column(String, nullable=True)
    status = Column(String, nullable=True)
    agency_id = Column(String, nullable=True)
    agency_name = Column(String, nullable=True)
    epa_region = Column(String, nullable=True)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    elevation = Column(Numeric(10, 6), nullable=True)
    gmt_offset = Column(Numeric(10, 6), nullable=True)
    country_fips = Column(String, nullable=True)
    cbsa_id = Column(String, nullable=True)
    cbsa_name = Column(String, nullable=True)
    state_aqs_code = Column(String, nullable=True)
    state_abbrev = Column(String, nullable=True)
    county_code = Column(String, nullable=True)
    county_name = Column(String, nullable=True)
    location_coord = Column(Geometry(geometry_type='POINT'), nullable=True)
