import pendulum
from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(
    schedule="@once",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["external_aq_data"]
)
def create_table_stations_waqi():
    """This dag runs a table script to create the fact table with World Air Quality Index data"""

    create_waqi_table = PostgresOperator(
        task_id="create_table_stations_waqi",
        postgres_conn_id="postgres_aq",
        sql="sql/create_table_stations_waqi.sql",
    )

create_table_stations_waqi()