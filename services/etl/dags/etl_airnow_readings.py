"""
airnow etl functions

for initial setup:
    1. run etl_airnow_stations dag
    2. run etl_airnow dag (the dag in this file)
    3. at some-hr:59 run load_prod_airnow_stations dag
"""
import os
from datetime import datetime as dt
from datetime import timedelta

import numpy as np
import pandas as pd
import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from config import Settings

settings = Settings()
params = {
    "startDate": dt.utcnow().strftime('%Y-%m-%dT%H'),
    "endDate": (dt.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H'),
    "parameters": "OZONE,PM25,PM10,CO,NO2,SO2",
    "BBOX": "-167.716404,3.233406,-63.653904,70.867976",
    "dataType": "B",
    "format": "text/csv",
    "verbose": "1",
    "monitorType": "2",
    "includerawconcentrations": "0",
    "API_KEY": settings.AIRNOW_API_KEY,
    }
AIRNOW_BY_STATION_API_URL = "https://www.airnowapi.org/aq/data/"


@dag(
    dag_id="etl_airnow",
    schedule=timedelta(minutes=10),
    start_date=dt(2022, 12, 2, 12, 2),
    catchup=False,
    dagrun_timeout=timedelta(minutes=2),
)
def airnow_etl():
    """
    First, creates temp table in postgres db. Then performs ETL of
    air quality data for all of USA for current hour."""
    create_temp_airnow_table = PostgresOperator(
        task_id="create_table_temp_airnow_readings",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_table_temp_airnow_readings.sql",
    )

    @task
    def extract_current_data():
        """extracts data from airnow api and stages it in csv file."""
        data_path = "/opt/airflow/dags/files/raw_airnow_data.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        response = requests.get(
            AIRNOW_BY_STATION_API_URL, params=params, timeout=20
            )
        csv_data = response.text
        with open(data_path, 'w') as file:
            file.write(csv_data)

    def reshape_airnow_data(df):
        """
        Uses .groupby() to split 'parameter' column into pm2.5 and pm10 groups.
        Then merge groups together under columns:

        site name | datetime | PM10 conc. | PM10 AQI |
        PM10 AQI cat. | PM2_5 conc. | PM2_5 AQI | PM2_5 AQI cat.
        """
        parameter_groups = df.groupby("parameter")
        pm10 = parameter_groups.get_group("PM10").drop(["parameter"], axis=1)
        pm10.rename(
            columns={
                "concentration": "pm_10_conc",
                "AQI": "pm_10_AQI",
                "AQI cat": "pm_10_cat"},
            inplace=True
        )
        pm2_5 = parameter_groups.get_group("PM2.5").drop(["parameter"], axis=1)
        pm2_5.rename(
            columns={
                "concentration": "pm_25_conc",
                "AQI": "pm_25_AQI",
                "AQI cat": "pm_25_AQI_cat"},
            inplace=True
        )
        merged_df = pd.merge(
            pm10,
            pm2_5,
            how="outer",
            on=["datetime", "station_name"],
            sort=False,
        )

        cols = merged_df.columns.tolist()
        cols = [cols[-4]] + cols[:4] + cols[-3:]
        merged_df = merged_df[cols]
        return merged_df

    @task
    def load_to_temp():
        """load new data to temp table"""
        column_names = [
            "latitude",
            "longitude",
            "datetime",
            "parameter",
            "concentration",
            "unit",
            "AQI",
            "AQI cat",
            "station_name",
            "agency name",
            "station id",
            "full station id", ]
        df = pd.read_csv(
            "/opt/airflow/dags/files/raw_airnow_data.csv", names=column_names,
        )
        df['station_name'].replace(r'^\s*$', np.nan, regex=True, inplace=True) #for rows with blank station names, fill station name with nan
        df.dropna(axis=0, inplace=True)
        df = df.drop(
            ["latitude", "longitude", "unit", "agency name", "station id",
             "full station id"],
            axis=1
        )
        df.to_csv(
            '/opt/airflow/dags/files/new_airnow_data.csv',
            header=True,
            index=False
            )
        merged_df = reshape_airnow_data(df)
        merged_df.drop_duplicates(['station_name', 'datetime'], keep='last', inplace=True)
        merged_df.replace({',': '-'}, regex=True, inplace=True)
        merged_df.replace(-999.0, np.nan, inplace=True)
        merged_df.to_csv(
            '/opt/airflow/dags/files/merged_airnow_data.csv',
            header=False,
            index=False
            )

        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        hook.copy_expert(
            sql="""
                COPY temp_airnow_data FROM stdin WITH DELIMITER AS ',' 
                NULL AS ''
                """,
            filename='/opt/airflow/dags/files/merged_airnow_data.csv')

    drop_CA_rows = PostgresOperator(
        task_id="drop_CA_rows",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/drop_rows_airnow.sql",
    )

    load_to_production = PostgresOperator(
        task_id="airnow_load_to_prod_data",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/load_prod_airnow_readings.sql",
    )


    create_temp_airnow_table >> extract_current_data() >> load_to_temp()
    load_to_temp() >> drop_CA_rows >> load_to_production


dag = airnow_etl()
