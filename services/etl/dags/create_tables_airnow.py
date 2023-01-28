"""airnow production table creation"""
import pendulum
from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(
    dag_id="create_tables_airnow",
    schedule='@once',
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
)

def create_tables_airnow():
    """
    Create production tables for airnow
    """
    create_table_readings_airnow = PostgresOperator(
        task_id="create_table_readings_airnow",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_table_readings_airnow.sql",
    )

    create_table_stations_airnow = PostgresOperator(
        task_id="create_table_stations_airnow",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_table_stations_airnow.sql",
    )

dag = create_tables_airnow()