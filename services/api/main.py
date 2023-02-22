"""api routes"""
from config import Settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router_stations
from routers import router_readings

# Base and models imported to be picked up by Alembic
from shared_models import Base
from shared_models import readings_airnow, stations_airnow


settings = Settings()

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_readings.router)
app.include_router(router_stations.router)


@app.get("/")
def root():
    return {"message": "ah poopy"}
