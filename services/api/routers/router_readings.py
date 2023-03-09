"""api data routes"""
from database import get_db
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .crud import crud
from shared_models.readings_airnow import ReadingsResponseModel
from shared_models.pydantic_models import TimeEnum

router = APIRouter(
    prefix="/air-readings",
    tags=["air-readings"],
)


@router.get("/from-ids/", response_model=list[ReadingsResponseModel])
def get_readings_from_ids(
    ids: list[str] = Query(), db: Session = Depends(get_db), period: TimeEnum = TimeEnum("all_time")
):
    """given ids and time period returns appropriate data readings"""
    data = crud.get_data(ids, db, period)
    return data
