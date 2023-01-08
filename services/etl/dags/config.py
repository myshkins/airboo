from functools import lru_cache

from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    POSTGRES_URI = "postgresql://airflow:airflow@postgres:5432/air_quality"
    WAQI_BASE_URL = "https://api.waqi.info/"
    WAQI_TOKEN = "bb10d851797e497b46823a5b4f984354c6ff4d9a"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf8'

@lru_cache()
def get_env_configs():
    return EnvSettings()