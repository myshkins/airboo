from sqlalchemy import (Column, DateTime, ForeignKey, Numeric, String,
                        relationship)

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
    station_id = Column(String, ForeignKey("stations_airnow.station_id"), primary_key=True, nullable=False)

    stations_rel = relationship("AirnowStations", backref="readings_airnow")


class ReadingsAirnowTemp(ReadingsAirnowCommon):
    __tablename__ = "readings_airnow_temp"
