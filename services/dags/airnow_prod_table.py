"""airnow production table creation"""
from datetime import datetime as dt
from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(
    dag_id="airnow_production_table_creation",
    schedule='@once',
    start_date=dt(2022, 12, 2, 18, 39)
)

def create_prod_table():
    """
    Create production table for airnow readings
    """
    create_airnow_table = PostgresOperator(
        task_id="create_airnow_prod_table",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_prod_airnow_table.sql",
    )

dag = create_prod_table()