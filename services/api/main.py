"""api routes"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from routers import router_readings, router_stations

# Base and models imported to be picked up by Alembic
from shared_models import Base
from shared_models import readings_airnow, stations_airnow


settings = Settings()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:9000",
    "http://airboo.ak0.io",
    "https://airboo.ak0.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_readings.router)
app.include_router(router_stations.router)


@app.get("/")
def root():
    return {"message": "hewo world"}


@app.get("/health-check")
def health_check():
    return {"message": "OK"}
