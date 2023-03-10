from pydantic import BaseSettings
from datetime import datetime


class Settings(BaseSettings):
    """config for api"""

    POSTGRES_URI: str
