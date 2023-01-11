"""api routes"""
from config import Settings
from fastapi import FastAPI
from routers import air_data, stations
from sqlalchemy import create_engine

settings = Settings()
engine = create_engine(settings.POSTGRES_URL, future=True)
app = FastAPI()


app.include_router(air_data.router)
app.include_router(stations.router)

@app.get("/")
def root():
    return {"message": "ah poop"}


