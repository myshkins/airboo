"""api routes"""
from config import Settings
from fastapi import FastAPI
from routers import router_stations
from routers import router_readings
from shared_models import Base


settings = Settings()

app = FastAPI()


app.include_router(router_readings.router)


app.include_router(router_stations.router)


@app.get("/")
def root():
    return {"message": "ah poop"}
