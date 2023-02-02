from db.models import Base
from sqlalchemy import Column, DateTime, Integer, Numeric, String


class Waqi_Stations(Base):
    __tablename__ = 'stations_waqi'

    station_id = Column(Integer, primary_key=True, nullable=False)
    station_name = Column(String, nullable=False)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    request_datetime = Column(DateTime, nullable=True)
    data_datetime = Column(DateTime, nullable=True)


class Waqi_Stations_Temp(Base):
    __tablename__ = 'stations_waqi_temp'

    station_id = Column(Integer, primary_key=True, nullable=False)
    station_name = Column(String, nullable=False)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    request_datetime = Column(DateTime, nullable=True)
    data_datetime = Column(DateTime, nullable=True)
