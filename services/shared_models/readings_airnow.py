from sqlalchemy import Column, DateTime, Numeric, String

from . import Base


class ReadingsAirnowCommon(Base):
    __abstract__ = True

    station_id = Column(String, primary_key=True, nullable=False)
    reading_datetime = Column(DateTime, primary_key=True, nullable=False)
    request_datetime = Column(DateTime, nullable=False)
    pm_10_conc = Column(Numeric(7, 3))
    pm_10_aqi = Column(Numeric(7, 3))
    pm_10_aqi_cat = Column(Numeric(2, 1))
    pm_25_conc = Column(Numeric(7, 3))
    pm_25_aqi = Column(Numeric(7, 3))
    pm_25_aqi_cat = Column(Numeric(2, 1))


class ReadingsAirnow(ReadingsAirnowCommon):
    __tablename__ = "readings_airnow"


class ReadingsAirnowTemp(ReadingsAirnowCommon):
    __tablename__ = "readings_airnow_temp"
