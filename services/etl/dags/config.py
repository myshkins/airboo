from pydantic import BaseSettings


class Settings(BaseSettings):
    """config for airflow"""
    AIRNOW_API_KEY: str

    class Config:
        env_file = '/opt/airflow/dags/.env.airflow'
        env_file_encoding = 'utf8'