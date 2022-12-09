import pendulum
from airflow.decorators import dag, task
from api_interface import get_waqi_data as gwd
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

@dag(
    schedule="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["external_aq_data"]
)
def waqi_dag():
    """This dag runs a table script to create the fact table with World Air Quality Index data"""

    create_pet_table = PostgresOperator(
        task_id="create_table_waqi",
        postgres_conn_id="AIRFLOW_CONN_POSTGRES",
        sql="sql/create_table_waqi.sql",
    )

waqi_dag()