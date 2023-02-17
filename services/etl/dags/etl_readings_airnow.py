"""
airnow etl functions

for initial setup:
    1. run etl_airnow_stations dag
    2. run etl_airnow dag (the dag in this file)
    3. after one hr run load_prod_airnow_stations dag
"""
import os
from datetime import timedelta

import pendulum
from airflow.decorators import dag, task
from api_interface import get_readings_airnow as gad
from db.db_engine import get_db
from logger import LOGGER
from shared_models.readings_airnow import ReadingsAirnowTemp
from util.util_sql import read_sql


@dag(
    dag_id="etl_readings_airnow",
    schedule=timedelta(minutes=10),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=timedelta(minutes=2),
)
def etl_airnow_readings():
    """
    This dag retrieves air quality data from airnow.org for all of USA for
    current hour."""

    @task
    def create_table_readings_airnow_temp():
        with get_db() as db:
            engine = db.get_bind()
            if engine.has_table("readings_airnow_temp"):
                ReadingsAirnowTemp.__table__.drop(db.get_bind())
            ReadingsAirnowTemp.__table__.create(db.get_bind())

    @task
    def extract_current_readings():
        """extracts data from airnow api and stages it in csv file."""
        data_path = "/opt/airflow/dags/files/raw_readings_airnow.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        csv_data = gad.get_readings_airnow()
        with open(data_path, "w") as file:
            file.write(csv_data)

    @task
    def load_temp():
        """loads everything to temp, data is very normalized here"""
        file_path = "/opt/airflow/dags/files/raw_readings_airnow.csv"
        with get_db() as db, open(file_path, mode="r") as file:
            load_stmt = read_sql("dags/sql/load_readings_airnow_temp.sql")
            cursor = db.connection().connection.cursor()
            cursor.copy_expert(load_stmt[0], file)
            db.commit()

    @task
    def load_prod():
        """upserts airnow readings to prod table"""
        stmt = read_sql("dags/sql/load_readings_airnow.sql")
        with get_db() as db:
            db.execute(stmt[0])
            db.commit()

    a = create_table_readings_airnow_temp()
    b = extract_current_readings()
    c = load_temp()
    d = load_prod()

    a >> b >> c >> d


etl_airnow_readings()
