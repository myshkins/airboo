from pydantic import BaseSettings


class Settings(BaseSettings):
    """config for airflow"""
    POSTGRES_URI: str
    WAQI_BASE_URL: str
    WAQI_TOKEN: str
    AIRNOW_API_KEY: str

    class Config:
        env_file = '/opt/airflow/dags/.env.airflow'
        env_file_encoding = 'utf8'
