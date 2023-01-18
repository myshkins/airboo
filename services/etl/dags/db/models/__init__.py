from db.db_engine import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Base.metadata.create_all(bind=engine)