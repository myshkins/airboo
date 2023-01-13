from pydantic import BaseSettings


class Settings(BaseSettings):
    """config for airflow"""
    POSTGRES_URI = "postgresql://airflow:airflow@postgres:5432/air_quality"
    WAQI_BASE_URL = "https://api.waqi.info/"
    WAQI_TOKEN = "bb10d851797e497b46823a5b4f984354c6ff4d9a"
    AIRNOW_API_KEY: str

    class Config:
        env_file = '/opt/airflow/dags/.env.airflow'
        env_file_encoding = 'utf8'