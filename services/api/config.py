from pydantic import BaseSettings


class Settings(BaseSettings):
    """config for api"""
    POSTGRES_URI: str

    class Config:
        env_file = '.env.api'
        env_file_encoding = 'utf8'
