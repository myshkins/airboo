"""sqlalchemy dependency for api routes"""
from config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = Settings()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()