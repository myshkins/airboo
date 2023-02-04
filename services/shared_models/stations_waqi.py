from sqlalchemy import Column, DateTime, Integer, Numeric, String

from . import Base


class Waqi_Stations_Common(Base):
    __abstract__ = True

    station_id = Column(Integer, primary_key=True, nullable=False)
    station_name = Column(String, nullable=False)
    latitude = Column(Numeric(10, 6), nullable=False)
    longitude = Column(Numeric(10, 6), nullable=False)
    request_datetime = Column(DateTime, nullable=True)
    data_datetime = Column(DateTime, nullable=True)


class Waqi_Stations(Waqi_Stations_Common):
    __tablename__ = "stations_waqi"


class Waqi_Stations_Temp(Waqi_Stations_Common):
    __tablename__ = "stations_waqi_temp"
