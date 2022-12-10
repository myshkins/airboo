"""daang look at that dag, it ETL"""

import csv
from datetime import datetime as dt, timedelta
import json
import os

import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

params = {
    "API_KEY": "AA5AB45D-9E64-41DE-A918-14578B9AC816",
    "zipCode": 11206,
    "format": "application/json"}
CURRENT_ZIP_BY_URL = "https://www.airnowapi.org/aq/observation/zipCode/current/"

@dag(
    dag_id="etl",
    schedule=timedelta(minutes=1),
    start_date=dt(2022, 12, 2, 18, 39),
    catchup=False,
    dagrun_timeout=timedelta(minutes=20),
)
def etl():
    create_airnow_table = PostgresOperator(
        task_id="create_AQI_table",
        postgres_conn_id="etl_pg_conn",
        sql="""
            CREATE TABLE IF NOT EXISTS airnow (
                datetime TEXT PRIMARY KEY,
                aqi TEXT
            );""",
    )

    create_airnow_temp_table = PostgresOperator(
        task_id="create_AQI_temp_table",
        postgres_conn_id='etl_pg_conn',
        sql="""
            DROP TABLE IF EXISTS airnow_temp;
            CREATE TABLE airnow_temp (
                datetime TEXT PRIMARY KEY,
                aqi TEXT
            );""",
    )

    @task
    def extract_current_data():
        date = dt.now()
        data_path = "/opt/airflow/dags/files/aqi_data.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        response = requests.get(CURRENT_ZIP_BY_URL, params=params)
        json_data = json.loads(response.text)
        ozone = json_data[0]["AQI"]
        data = (date, ozone)
        # pm2_5 = json_data[1]["AQI"]
        # pm10 = json_data[2]["AQI"]
        with open(data_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        
        hook = PostgresHook(postgres_conn_id="etl_pg_conn")
        hook.copy_expert(
            sql="COPY airnow_temp FROM stdin WITH DELIMITER as ','",
            filename='/opt/airflow/dags/files/aqi_data.csv')
    
    [create_airnow_table, create_airnow_temp_table] >> extract_current_data()

dag = etl()
