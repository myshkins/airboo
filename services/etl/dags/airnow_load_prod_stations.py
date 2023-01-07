"""airnow etl functions"""
from datetime import timedelta, datetime as dt

from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


@dag(
    dag_id="airnow_load_prod_stations",
    schedule=timedelta(days=1),
    start_date=dt(2022, 12, 1, 12, 57),
    catchup=False,
    dagrun_timeout=timedelta(minutes=2),
)
def airnow_load_prod_stations():
    """
    Dag to trim and load temp_airnow_stations to prod_airnow_stations
    """
    airnow_trim_stations = PostgresOperator(
        task_id="airnow_trim_stations",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/airnow_trim_stations.sql"
    )

    airnow_load_prod_stations = PostgresOperator(
        task_id="airnow_load_prod_stations",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/airnow_load_prod_stations.sql",
    )

    airnow_trim_stations >> airnow_load_prod_stations

dag = airnow_load_prod_stations()