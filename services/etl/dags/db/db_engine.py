from contextlib import contextmanager

from config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(Settings().POSTGRES_URI)
# engine = create_engine("postgresql://airflow:airflow@postgres:5432/air_quality")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
