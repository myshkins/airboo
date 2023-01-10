"""api routes"""
from functools import lru_cache

from fastapi import FastAPI
from sqlalchemy import create_engine, text
from config import Settings

from routers import air_data, stations

settings = Settings()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, future=True)
app = FastAPI()


app.include_router(air_data.router)
app.include_router(stations.router)

@app.get("/")
def root():
    return {"message": "ah poop"}


