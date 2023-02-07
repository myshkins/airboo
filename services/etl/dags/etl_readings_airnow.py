"""
airnow etl functions

for initial setup:
    1. run etl_airnow_stations dag
    2. run etl_airnow dag (the dag in this file)
    3. after one hr run load_prod_airnow_stations dag
"""
import os
from datetime import timedelta

import numpy as np
import pandas as pd
import pendulum
from airflow.decorators import dag, task
from api_interface import get_readings_airnow as gad
from db.db_engine import get_db
from util.util_sql import read_sql
from shared_models.readings_airnow import ReadingsAirnowTemp


@dag(
    dag_id="etl_readings_airnow",
    schedule=timedelta(minutes=10),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=timedelta(minutes=2),
)
def etl_airnow_readings():
    """
    This dag retrieves air quality data from airnow.org for all of USA for
    current hour."""

    @task
    def create_table_readings_airnow_temp():
        with get_db() as db:
            engine = db.get_bind()
            if engine.has_table("readings_airnow_temp"):
                ReadingsAirnowTemp.__table__.drop(db.get_bind())
            ReadingsAirnowTemp.__table__.create(db.get_bind())

    @task
    def extract_current_readings():
        """extracts data from airnow api and stages it in csv file."""
        data_path = "/opt/airflow/dags/files/raw_readings_airnow.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        csv_data = gad.get_readings_airnow()
        with open(data_path, "w") as file:
            file.write(csv_data)

    @task
    def transform_airnow_readings():
        """
        Cleans data. Then, uses .groupby() to split 'parameter' column into
        pm2.5 and pm10 groups.Then merge groups together under columns:
        site name | reading_datetime | pm10_conc | pm10_aqi | pm10_aqi_cat |
        pm2_5_conc | pm2_5_aqi | pm2_5_aqi_cat
        """
        column_names = [
            "latitude",
            "longitude",
            "reading_datetime",
            "parameter",
            "concentration",
            "unit",
            "aqi",
            "aqi_cat",
            "station_name",
            "agency_name",
            "station_id",
            "full_station_id",
        ]
        df = pd.read_csv(
            "/opt/airflow/dags/files/raw_readings_airnow.csv",
            names=column_names,
        )
        # for rows with blank station names, fill station name with nan
        df["station_id"].replace(r"^\s*$", np.nan, regex=True, inplace=True)
        df.dropna(axis=0, inplace=True)
        df.drop(
            [
                "latitude",
                "longitude",
                "unit",
                "agency_name",
                "station_name",
                "full_station_id",
            ],
            axis=1,
            inplace=True,
        )
        parameter_groups = df.groupby("parameter")
        pm10 = parameter_groups.get_group("PM10").drop(["parameter"], axis=1)
        pm10.rename(
            columns={
                "concentration": "pm_10_conc",
                "aqi": "pm_10_aqi",
                "aqi_cat": "pm_10_cat",
            },
            inplace=True,
        )
        pm2_5 = parameter_groups.get_group("PM2.5").drop(["parameter"], axis=1)
        pm2_5.rename(
            columns={
                "concentration": "pm_25_conc",
                "aqi": "pm_25_aqi",
                "aqi_cat": "pm_25_aqi_cat",
            },
            inplace=True,
        )
        merged_df = pd.merge(
            pm10,
            pm2_5,
            how="outer",
            on=["reading_datetime", "station_id"],
            sort=False,
        )
        df.to_csv("/opt/airflow/dags/files/a_rds_2.csv", header=True, index=False)
        merged_df = merged_df.assign(request_datetime=pendulum.now(tz="UTC"))
        cols = [
            "station_id",
            "request_datetime",
            "reading_datetime",
            "pm_10_conc",
            "pm_10_aqi",
            "pm_10_cat",
            "pm_25_conc",
            "pm_25_aqi",
            "pm_25_aqi_cat",
        ]
        merged_df = merged_df[cols]
        merged_df.replace({",": "-"}, regex=True, inplace=True)
        merged_df.replace(-999.0, np.nan, inplace=True)
        merged_df.drop_duplicates(["station_id"], inplace=True)
        merged_df.to_csv(
            "/opt/airflow/dags/files/merged_readings_airnow.csv",
            header=False,
            index=False,
        )

    @task
    def load_readings_airnow_temp():
        """load new readings to temp table"""
        with get_db() as db:
            path = "/opt/airflow/dags/files/merged_readings_airnow.csv"
            with open(path, mode="r") as file:
                stmt = read_sql("dags/sql/load_readings_airnow_temp.sql")
                cursor = db.connection().connection.cursor()
                cursor.copy_expert(stmt[0], file)
            db.commit()

    @task
    def drop_canada_rows():
        """drops canada rows from readings"""
        stmt = read_sql("dags/sql/drop_rows_airnow.sql")
        with get_db() as db:
            db.execute(stmt[0])
            db.commit()

    @task
    def load_readings_airnow():
        """upserts airnow readings to prod table"""
        stmt = read_sql("dags/sql/load_readings_airnow.sql")
        with get_db() as db:
            db.execute(stmt[0])
            db.commit()

    a = create_table_readings_airnow_temp()
    b = extract_current_readings()
    c = transform_airnow_readings()
    d = load_readings_airnow_temp()
    e = drop_canada_rows()
    f = load_readings_airnow()

    a >> b >> c >> d >> e >> f


etl_airnow_readings()
