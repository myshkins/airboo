"""api data routes"""
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .crud import crud
from shared_models.stations_airnow import StationsAirnowPydantic


router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/all-nearby/", response_model=list[StationsAirnowPydantic])
def get_nearby_stations(zipcode: str, db: Session = Depends(get_db)):
    """given zipcode, returns the 5 nearest stations"""
    station_list = crud.get_nearby_stations(zipcode, db)
    if station_list == 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="invalid zipcode"
        )
    return station_list


# needs test
@router.get("/first-closest")
def get_first_station(zipcode: str, db: Session = Depends(get_db)):
    """given zipcode, returns first closest station"""
    closest = crud.get_closest_station(zipcode, db)
    return closest
