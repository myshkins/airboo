from sqlalchemy import Column, DateTime, Numeric, String

from . import Base


class Readings_Airnow(Base):
    __tablename__ = 'readings_airnow'

    station_name = Column(String, primary_key=True, nullable=False)
    reading_datetime = Column(DateTime, primary_key=True, nullable=False)
    request_datetime = Column(DateTime, nullable=False)
    pm_10_conc = Column(Numeric(7, 3))
    pm_10_AQI = Column(Numeric(7, 3))
    pm_10_AQI_CAT = Column(Numeric(2, 1))
    pm_25_conc = Column(Numeric(7, 3))
    pm_25_AQI = Column(Numeric(7, 3))
    pm_25_AQI_CAT = Column(Numeric(2, 1))
