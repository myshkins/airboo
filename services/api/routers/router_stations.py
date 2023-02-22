"""api data routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .crud import crud
from database import get_db

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/all-nearby/")
def get_nearby_stations(zipcode: str, db: Session = Depends(get_db)):
    """given zipcode, returns the 5 nearest stations"""
    return crud.get_nearby_stations(zipcode, db)


@router.get("/first-closest")
def get_first_station(zipcode: str, db: Session = Depends(get_db)):
    """given zipcode, returns first closest station"""
    closest = crud.get_closest_station(zipcode, db)
    return closest
