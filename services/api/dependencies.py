"""sqlalchemy dependency for api routes"""
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://airflow:airflow@postgres/airnow"
router = APIRouter()

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
