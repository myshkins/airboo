"""airnow production table creation"""
from datetime import datetime as dt

from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(
    dag_id="airnow_production_table_creation",
    schedule='@once',
    start_date=dt(2022, 12, 2, 18, 39)
)

def create_prod_tables():
    """
    Create production table for airnow readings
    """
    create_prod_airnow_data_table = PostgresOperator(
        task_id="create_prod_airnow_data_table",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_prod_airnow_data_table.sql",
    )

    create_prod_airnow_station_table = PostgresOperator(
        task_id="create_prod_airnow_station_table",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_prod_airnow_station_table.sql",
    )

dag = create_prod_tables()