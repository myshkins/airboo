"""airnow production table creation"""
import pendulum
from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(
    dag_id="create_table_prod_airnow_readings",
    schedule='@once',
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
)

def create_prod_tables():
    """
    Create production table for airnow readings
    """
    create_prod_airnow_data_table = PostgresOperator(
        task_id="create_prod_airnow_data_table",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_table_prod_airnow_readings.sql",
    )

    create_prod_airnow_station_table = PostgresOperator(
        task_id="create_prod_airnow_station_table",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_table_prod_airnow_stations.sql",
    )

dag = create_prod_tables()