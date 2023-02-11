from shared_models import Base
from sqlalchemy import (TIMESTAMP, Column, DateTime, Identity, Integer,
                        Numeric, String, text)


class ReadingsAirnow(Base):
    __tablename__ = "readings_airnow"

    full_aqs_id = Column(String, primary_key=True, nullable=False)
    reading_datetime = Column(DateTime, primary_key=True, nullable=False)
    data_datetime = Column(
        TIMESTAMP(),
        server_default=text("now()"),
        nullable=False)
    pm25_conc = Column(Numeric(7, 3))
    pm25_aqi = Column(Integer, nullable=True)
    pm25_cat = Column(Integer, nullable=True)
    pm10_conc = Column(Numeric(7, 3))
    pm10_aqi = Column(Integer, nullable=True)
    pm10_cat = Column(Integer, nullable=True)
    o3_conc = Column(Numeric(7, 3))
    o3_aqi = Column(Integer, nullable=True)
    o3_cat = Column(Integer, nullable=True)
    co_conc = Column(Numeric(7, 3))
    co_aqi = Column(Integer, nullable=True)
    co_cat = Column(Integer, nullable=True)
    no2_conc = Column(Numeric(7, 3))
    no2_aqi = Column(Integer, nullable=True)
    no2_cat = Column(Integer, nullable=True)
    so2_conc = Column(Numeric(7, 3))
    so2_aqi = Column(Integer, nullable=True)
    so2_cat = Column(Integer, nullable=True)


class ReadingsAirnowTemp(Base):
    __tablename__ = "readings_airnow_temp"

    readings_temp_pk = Column(
        Integer,
        Identity(start=1, cycle=False),
        primary_key=True)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    timestamp_utc = Column(String, nullable=False)
    pollutant = Column(String, nullable=True)
    concentration = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    aqi = Column(String, nullable=True)
    category = Column(String, nullable=True)
    site_name = Column(String, nullable=True)
    site_agency = Column(String, nullable=True)
    aqs_id = Column(String, nullable=True)
    full_aqs_id = Column(String, nullable=True)
