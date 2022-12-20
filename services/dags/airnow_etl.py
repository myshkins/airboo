"""airnow etl functions"""
from datetime import datetime as dt, timedelta
import os

import pandas as pd
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
    "includerawconcentrations": "0",
    "API_KEY": "AA5AB45D-9E64-41DE-A918-14578B9AC816",
    }
AIRNOW_BY_STATION_API_URL = "https://www.airnowapi.org/aq/data/"


@dag(
    dag_id="airnow_etl",
    schedule=timedelta(minutes=1),
    start_date=dt(2022, 12, 2, 18, 39),
    catchup=False,
    dagrun_timeout=timedelta(minutes=2),
)
def airnow_etl():
    """
    First, creates temp table in postgres db. Then performs ETL of
    air quality data for all of USA for current observations."""
    create_airnow_tables = PostgresOperator(
        task_id="create_airnow_temp_table",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_temp_airnow_table.sql",
    )

    @task
    def extract_current_data():
        """extracts data from airnow api and stages it in csv file."""
        data_path = "/opt/airflow/dags/files/aqi_data.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        response = requests.get(
            AIRNOW_BY_STATION_API_URL, params=params, timeout=20
            )
        csv_data = response.text
        with open(data_path, 'w') as file:
            file.write(csv_data)
    
    def regroup_pm25_pm10(df):
        """
        Uses .groupby() to split 'parameter' column into pm2.5 and pm10 groups.
        Then merge groups together under columns:
        
        site name | lat | long | datetime | PM10 conc. | PM10 AQI |
        PM10 AQI cat. | PM2_5 conc. | PM2_5 AQI | PM2_5 AQI cat.
        """
        parameter_groups = df.groupby("parameter")
        pm10 = parameter_groups.get_group("PM10").drop(["parameter"], axis=1)
        pm10.rename(
            columns={
                "concentration": "PM10 conc.",
                "AQI": "PM10 AQI", "AQI cat.":
                "PM10 AQI cat"},
                inplace=True)
        pm2_5 = parameter_groups.get_group("PM2.5").drop(["parameter"], axis=1)
        pm2_5.rename(
            columns={
                "concentration": "PM2_5 conc.",
                "AQI": "PM2_5 AQI",
                "AQI cat": "PM2_5 AQI cat."},
                inplace=True)
        merged_df = pd.merge(
            pm10,
            pm2_5,
            how="outer",
            on=["latitude", "longitude", "datetime", "site name"],
        )

        cols = merged_df.columns.tolist()
        cols = [cols[-4]] + cols[:6] + cols[-3:]
        merged_df = merged_df[cols]
        return merged_df

    def clean_string_values(df):
        """
        changes string values that include quotations and commas. eg.:
        "Rangely, CO"  --> Rangely_CO
        """
        df["site name"] = df["site name"].str.replace(',', '-')
        return df

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
            "site name",
            "agency name",
            "station id",
            "full station id",]
        df = pd.read_csv(
            "/opt/airflow/dags/files/aqi_data.csv", names=column_names,
            )
        df.dropna(axis=0)
        df = df.drop(
            ["unit", "agency name", "station id", "full station id"], axis=1
            )
        merged_df = regroup_pm25_pm10(df)
        merged_df = clean_string_values(merged_df)
        merged_df.to_csv('/opt/airflow/dags/files/aqi_data.csv', header=False, index=False)

        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        hook.copy_expert(
            sql="COPY airnow_readings_temp FROM stdin WITH DELIMITER as ',' NULL AS ''",
            filename='/opt/airflow/dags/files/aqi_data.csv')

    @task
    def load_to_production():
        """upsert new data to the production table"""
        
        query = """
            INSERT INTO airnow_readings
            SELECT * FROM airnow_readings_temp
            ON CONFLICT DO NOTHING/UPDATE
        """
        try:
            hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
            conn = hook.get_conn()
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            return 0
        except Exception as e:
            return 1

    create_airnow_tables >> extract_current_data() >> load_to_temp() >> load_to_production()


dag = airnow_etl()
