"""airnow dag for loading station data to production table"""
import pendulum
from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(
    dag_id="load_prod_airnow_stations",
    schedule=pendulum.duration(days=1),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=pendulum.duration(minutes=2),
)
def airnow_load_prod_stations():
    """
    Dag to trim and load temp_airnow_stations to prod_airnow_stations
    """
    airnow_trim_stations = PostgresOperator(
        task_id="airnow_trim_stations",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/trim_airnow_stations.sql"
    )

    airnow_load_prod_stations = PostgresOperator(
        task_id="airnow_load_prod_stations",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/load_prod_airnow_stations.sql",
    )

    airnow_trim_stations >> airnow_load_prod_stations

dag = airnow_load_prod_stations()