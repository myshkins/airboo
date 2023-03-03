from pydantic import BaseSettings


class Settings(BaseSettings):
    """config for api"""

    AQ_POSTGRES_URI: str
