# """api data routes"""
from database import get_db
from fastapi import APIRouter, Depends, Query
from shared_models.pydantic_models import PollutantEnum, TimeEnum, PollutantResponse
from shared_models.readings_airnow import ReadingsResponseModel
from sqlalchemy.orm import Session

from .crud import crud

router = APIRouter(
    prefix="/api/air-readings",
    tags=["air-readings"],
)


@router.get("/from-ids/", response_model=list[ReadingsResponseModel])
def get_readings_from_ids(
    ids: list[str] = Query(),
    db: Session = Depends(get_db),
    period: TimeEnum = TimeEnum("all_time"),
    pollutants: list[PollutantEnum] = Query(
        [
            PollutantEnum("pm25"),
        ]
    ),
):
    """given ids and time period returns appropriate data readings"""
    data = crud.get_data(ids, db, period, pollutants)
    return data


@router.get("/pollutants/", response_model=PollutantResponse)
def get_pollutants(ids: list[str] = Query(), db: Session = Depends(get_db)):
    """give ids returns dict of pollutants available for each station"""
    pollutants = crud.get_pollutants(ids, db)
    response = {"pollutants": pollutants}
    return response
