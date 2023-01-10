"""api data routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud
from dependencies import get_db


router = APIRouter(
    prefix="/air-data",
    tags=["air-data"],
)

@router.get("/from-closest/")
def get_data_from_closest(zipcode: str, db: Session = Depends(get_db)):
    station_data = crud.get_closest_station(zipcode, db)
    station = station_data[0][0]
    data = crud.get_data(station, db)
    return data
