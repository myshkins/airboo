"""airnow dag for ingesting station data"""
from datetime import timedelta

import pendulum
from airflow.decorators import dag, task
from api_interface import get_readings_airnow as gad
from db.db_engine import get_db
from shared_models.stations_airnow import AirnowStationsTemp
from util.util_sql import exec_sql, read_sql

PATH = "/opt/airflow/dags/"


@dag(
    dag_id="etl_stations_airnow",
    schedule=timedelta(hours=12),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=pendulum.duration(minutes=5),
)
def etl_stations_airnow():
    """
    Dag definition for pulling airnow station data, shaping that data, and
    putting it into the station table.
    """

    @task
    def create_table_stations_airnow_temp():
        """create temp table for airnow stations"""
        with get_db() as db:
            engine = db.get_bind()
            if engine.has_table("stations_airnow_temp"):
                AirnowStationsTemp.__table__.drop(db.get_bind())
            AirnowStationsTemp.__table__.create(db.get_bind())

    @task
    def get_stations_airnow():
        """gets station data file from airnow.org and writes it to .csv"""
        with open(f"{PATH}files/stations_airnow.csv", mode="w") as file:
            data = gad.get_stations_airnow()
            file.write(data)

    @task
    def load_temp_table():
        """get airnow stations and load everything into temp table"""
        file_path = '/opt/airflow/dags/files/stations_airnow.csv'
        with get_db() as db, open(file_path, mode='r') as file:
            load_stmt = read_sql('/opt/airflow/dags/sql/load_stations_airnow_temp.sql')
            cursor = db.connection().connection.cursor()
            cursor.copy_expert(load_stmt[0], file)
            db.commit()

    @task
    def load_prod():
        load_stmt = read_sql(
            '/opt/airflow/dags/sql/load_stations_airnow.sql')
        exec_sql(load_stmt)

    a = create_table_stations_airnow_temp()
    b = get_stations_airnow()
    c = load_temp_table()
    d = load_prod()

    a >> b >> c >> d


etl_stations_airnow()
