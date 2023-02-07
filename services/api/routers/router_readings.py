"""api data routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .crud import crud
from database import get_db


router = APIRouter(
    prefix="/air-data",
    tags=["air-data"],
)


@router.get("/from-closest/")
def get_data_from_closest(zipcode: str, db: Session = Depends(get_db)):
    station_data = crud.get_closest_station(zipcode, db)
    station_id = station_data[0][0]
    data = crud.get_data(station_id, db)
    return data
