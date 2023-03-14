from pydantic import BaseSettings


class Settings(BaseSettings):
    """config for api"""

    POSTGRES_URI: str
