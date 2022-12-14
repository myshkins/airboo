"""daang look at that dag, it ETL"""

# import csv
from datetime import datetime as dt, timedelta
import os

import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.connection import Connection


params = {
    "startDate": dt.utcnow().strftime('%Y-%m-%dT%H'),
    "endDate": (dt.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H'),
    "parameters": "OZONE,PM25,PM10,CO,NO2,SO2",
    "BBOX": "-124.205070,28.716781, -75.337882,45.419415",
    "dataType": "B",
    "format": "text/csv",
    "verbose": "1",
    "monitorType": "2",
    "includerawconcentrations": "1",
    "API_KEY": os.environ.get("AIRNOW_KEY"),
    }
AIRNOW_BY_STATION_API_URL = "https://www.airnowapi.org/aq/data/"


conn = Connection(
    conn_id="postgres_etl_conn",
    conn_type="postgres",
    description="connection for ingesting data to postgres",
    host="postgres",
    login="airflow",
    password="airflow",
    # extra=json.dumps(dict(this_param="some val", that_param="other val*")),
)

@dag(
    dag_id="el",
    schedule=timedelta(minutes=5),
    start_date=dt(2022, 12, 2, 18, 39),
    catchup=False,
    dagrun_timeout=timedelta(minutes=2),
)
def airnow_etl():
    """
    First, creates temp and final tables in postgres db. Then performs ETL of
    air quality data for all of USA for current observation."""
    create_airnow_tables = PostgresOperator(
        task_id="create_AQI_table",
        postgres_conn_id="AIRFLOW_CONN_POSTGRES",
        sql="create_airnow_table.sql",
    )

    @task
    def extract_current_data():
        """extracts data from airnow api and stages it in csv file."""
        data_path = "/opt/airflow/dags/files/aqi_data.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        response = requests.get(AIRNOW_BY_STATION_API_URL, params=params, timeout=20)
        csv_data = response.text
        with open(data_path, 'w') as file:
            file.write(csv_data)
    
    @task
    def load_to_temp():
        """load any new data from csv to temp table"""
        # use pandas to validate data here
        # also pandas to combine pm2.5 and pm10
        
        hook = PostgresHook(postgres_conn_id=conn.conn_id)
        hook.copy_expert(
            sql="COPY airnow_temp FROM stdin WITH DELIMITER as ','",
            filename='/opt/airflow/dags/files/aqi_data.csv')
    
    @task
    def transform_and_load():
        """transform(compare for new data) and load into production table"""


    # create_airnow_tables >> extract_current_data()


dag = airnow_etl()

