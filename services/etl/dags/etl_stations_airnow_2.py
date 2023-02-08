"""airnow dag for ingesting station data"""
from datetime import timedelta

import pendulum
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from api_interface import get_readings_airnow as gad
from db.db_engine import get_db
from shared_models.stations_airnow import AirnowStationsTemp
from util.util_sql import exec_sql, read_sql


@dag(
    dag_id="etl_stations_airnow_2",
    schedule=timedelta(hours=12),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=pendulum.duration(minutes=5),
)
def etl_stations_airnow_2():
    """
    Dag definition for pulling airnow station data, shaping that data, and
    putting it into the station table.
    """
    @task
    def create_table_stations_airnow_temp():
        """create temp table for airnow stations"""
        with get_db() as db:
            engine = db.get_bind()
            if engine.has_table('stations_airnow_temp'):
                AirnowStationsTemp.__table__.drop(db.get_bind())
            AirnowStationsTemp.__table__.create(db.get_bind())

    @task
    def get_stations_airnow():
        """gets station data file from airnow.org and writes it to .csv"""
        with open(
                '/opt/airflow/dags/files/stations_airnow.csv',
                mode='w') as file:
            data = gad.get_stations_airnow()
            file.write(data)

    @task
    def load_temp_table():
        """get airnow stations and load everything into temp table"""
        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        load_stmt = read_sql('/opt/airflow/dags/sql/copy_stations_airnow_temp.sql')
        hook.copy_expert(
            sql=load_stmt[0],
            filename='/opt/airflow/dags/files/stations_airnow.csv')

    @task
    def update_coords():
        coord_stmt = read_sql(
            '/opt/airflow/dags/sql/populate_station_coord_airnow_2.sql')
        exec_sql(coord_stmt)

    a = create_table_stations_airnow_temp()
    b = get_stations_airnow()
    c = load_temp_table()
    d = update_coords()

    a >> b >> c >> d


etl_stations_airnow_2()
