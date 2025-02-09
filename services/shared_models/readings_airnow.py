from datetime import datetime
from typing import Union, List
from . import Base
from pydantic import BaseModel
from sqlalchemy import (
    TIMESTAMP,
    Column,
    DateTime,
    Identity,
    Integer,
    Numeric,
    String,
    text,
)


class ReadingsAirnow(Base):
    __tablename__ = "readings_airnow"

    station_id = Column(String, primary_key=True, nullable=False)
    reading_datetime = Column(DateTime, primary_key=True, nullable=False)
    data_datetime = Column(TIMESTAMP(), server_default=text("now()"), nullable=False)
    pm25_aqi = Column(Integer, nullable=True)
    pm25_conc = Column(Numeric(7, 3))
    pm25_cat = Column(Integer, nullable=True)
    pm10_aqi = Column(Integer, nullable=True)
    pm10_conc = Column(Numeric(7, 3))
    pm10_cat = Column(Integer, nullable=True)
    o3_aqi = Column(Integer, nullable=True)
    o3_conc = Column(Numeric(7, 3))
    o3_cat = Column(Integer, nullable=True)
    co_aqi = Column(Integer, nullable=True)
    co_conc = Column(Numeric(7, 3))
    co_cat = Column(Integer, nullable=True)
    no2_aqi = Column(Integer, nullable=True)
    no2_conc = Column(Numeric(7, 3))
    no2_cat = Column(Integer, nullable=True)
    so2_aqi = Column(Integer, nullable=True)
    so2_conc = Column(Numeric(7, 3))
    so2_cat = Column(Integer, nullable=True)


class ReadingsAirnowTemp(Base):
    __tablename__ = "readings_airnow_temp"

    readings_temp_pk = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
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


class ReadingsAirnowPydantic(BaseModel):
    reading_datetime: Union[datetime, None] = None
    pm25_aqi: Union[int, None] = None
    pm25_conc: Union[float, None] = None
    pm25_cat: Union[int, None] = None
    pm10_aqi: Union[int, None] = None
    pm10_conc: Union[float, None] = None
    pm10_cat: Union[int, None] = None
    o3_aqi: Union[int, None] = None
    o3_conc: Union[float, None] = None
    o3_cat: Union[int, None] = None
    co_conc: Union[float, None] = None
    # note not co_aqi or co_cat because it's always null for co
    no2_aqi: Union[int, None] = None
    no2_conc: Union[float, None] = None
    no2_cat: Union[int, None] = None
    so2_aqi: Union[int, None] = None
    so2_conc: Union[float, None] = None
    so2_cat: Union[int, None] = None


class Reading(BaseModel):
    reading_datetime: datetime
    pollutant: str
    value: int


class ReadingsResponseModel(BaseModel):
    station_id: str
    pollutant: str
    readings: Union[List[Reading], List] = None
