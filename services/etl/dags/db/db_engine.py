from contextlib import contextmanager

from config import Settings
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

engine = create_engine(Settings().POSTGRES_AQ_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()