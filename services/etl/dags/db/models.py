from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Readings_WAQI_Temp(Base):
    __tablename__ = 'readings_waqi_temp'

    station_name = Column(String, primary_key=True, nullable=False)
    latitude = Column(Numeric(10,6))
    longitude = Column(Numeric(10,6))
    pm_10 = Column(Numeric(7,3))
    pm_25 = Column(Numeric(7,3))
    co = Column(Numeric(7,3))
    h = Column(Numeric(7,3))
    no2 = Column(Numeric(7,3))
    o3 = Column(Numeric(7,3))
    p = Column(Numeric(7,3))
    so2 = Column(Numeric(7,3))
    t = Column(Numeric(7,3))
    w = Column(Numeric(7,3))
    wg = Column(Numeric(7,3))
    reading_datetime = Column(DateTime, nullable=False)
    request_datetime = Column(DateTime, nullable=False)

class Stations_WAQI_Temp(Base):
    __tablename__ = 'stations_waqi_temp'

    station_id = Column(Integer, primary_key=True, nullable=False)
    station_name = Column(String, nullable=False)
    latitude = Column(Numeric(10,6), nullable=False)
    longitude = Column(Numeric(10,6), nullable=False)
    request_datetime = Column(DateTime, nullable=False)
    data_datetime = Column(DateTime, nullable=False)