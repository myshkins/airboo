from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, Numeric, String

from . import Base


class AirnowStations(Base):
    __tablename__ = "stations_airnow"

    full_aqs_id = Column(String, primary_key=True, nullable=False)
    station_id = Column(String, nullable=False)
    station_name = Column(String, nullable=False)
    agency_name = Column(String, nullable=False)
    status = Column(String, nullable=True)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    elevation = Column(Numeric(10, 6), nullable=True)
    country_fips = Column(String, nullable=True)
    location_coord = Column(Geometry(geometry_type="POINT"), nullable=True)


class AirnowStationsTemp(Base):
    __tablename__ = "stations_airnow_temp"

    station_temp_pk = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    station_id = Column(String, nullable=True)
    aqs_id = Column(String, nullable=True)
    full_aqs_id = Column(String, nullable=True)
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
