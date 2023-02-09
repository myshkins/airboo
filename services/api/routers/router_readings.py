"""api data routes"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .crud import crud
from database import get_db


router = APIRouter(
    prefix="/air-readings",
    tags=["air-readings"],
)


class IdList(BaseModel):
    ids: list[str]


@router.get("/from-closest/")
def get_data_from_closest(zipcode: str, db: Session = Depends(get_db)):
    station_data = crud.get_closest_station(zipcode, db)
    station_id = station_data[0][0]
    data = crud.get_data(station_id, db)
    return data


@router.get("/from-ids/")
def get_readings_from_ids(ids: IdList, db: Session = Depends(get_db)):
    data = crud.get_data(ids, db)
    return data