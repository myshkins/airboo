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
from api_interface import get_airnow_data as gad
from db.db_engine import get_db
from util.util_sql import read_sql, exec_sql 


@dag(
    dag_id="etl_airnow",
    schedule=timedelta(minutes=10),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=timedelta(minutes=2),
)
def airnow_etl():
    """
    This dag retrieves air quality data from airnow.org for all of USA for
    current hour."""
    
    @task
    def create_table_temp_airnow():
        sql_stmts = read_sql('dags/sql/create_table_temp_airnow_readings.sql')
        exec_sql(sql_stmts)

    @task
    def extract_current_data():
        """extracts data from airnow api and stages it in csv file."""
        data_path = "/opt/airflow/dags/files/raw_airnow_data.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        csv_data = gad.get_airnow_data()
        with open(data_path, 'w') as file:
            file.write(csv_data)

    @task
    def transform_airnow_data():
        """
        Cleans data. Then, uses .groupby() to split 'parameter' column into 
        pm2.5 and pm10 groups.Then merge groups together under columns: 
        site name | reading_datetime | PM10 conc. | PM10 AQI | PM10 AQI cat. |
        PM2_5 conc. | PM2_5 AQI | PM2_5 AQI cat.
        """
        column_names = [
            "latitude", "longitude", "reading_datetime", "parameter", "concentration",
            "unit", "AQI", "AQI cat", "station_name", "agency name", 
            "station id", "full station id",]
        df = pd.read_csv(
            "/opt/airflow/dags/files/raw_airnow_data.csv", names=column_names,
        )
        df['station_name'].replace(r'^\s*$', np.nan, regex=True, inplace=True) #for rows with blank station names, fill station name with nan
        df.dropna(axis=0, inplace=True)
        df.drop(
            ["latitude", "longitude", "unit", "agency name", "station id",
             "full station id"],
            axis=1,
            inplace=True,
        )
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
            on=["reading_datetime", "station_name"],
            sort=False,
        )
        merged_df = merged_df.assign(request_datetime=pendulum.now(tz='UTC'))
        cols = [
        'station_name', 'request_datetime', 'reading_datetime', 'pm_10_conc',
        'pm_10_AQI', 'pm_10_cat', 'pm_25_conc', 'pm_25_AQI', 'pm_25_AQI_cat'
        ]
        merged_df = merged_df[cols]
        merged_df.replace({',': '-'}, regex=True, inplace=True)
        merged_df.replace(-999.0, np.nan, inplace=True)
        merged_df.drop_duplicates(['station_name'], inplace=True)
        merged_df.to_csv(
            '/opt/airflow/dags/files/merged_airnow_data.csv',
            header=False,
            index=False
            )

    @task
    def load_readings_temp_airnow():
        """load new readings to temp table"""
        with get_db() as db:
            path = '/opt/airflow/dags/files/merged_airnow_data.csv'
            with open(path, mode='r') as file:
                stmt = read_sql('dags/sql/load_temp_airnow_readings.sql')
                cursor = db.connection().connection.cursor()
                cursor.copy_expert(stmt[0], file)
            db.commit()
    
    @task
    def drop_canada_rows():
        """drops canada rows from readings"""
        stmt = read_sql('dags/sql/drop_rows_airnow.sql')
        with get_db() as db:
            db.execute(stmt[0])
            db.commit()

    @task
    def load_readings_prod_airnow():
        """upserts airnow readings to prod table"""
        stmt = read_sql('dags/sql/load_prod_airnow_readings.sql')
        with get_db() as db:
            db.execute(stmt[0])
            db.commit()


    a = create_table_temp_airnow()
    b = extract_current_data()
    c = transform_airnow_data()
    d = load_readings_temp_airnow()
    e = drop_canada_rows()
    f = load_readings_prod_airnow()

    a >> b >> c >> d >> e >> f


dag = airnow_etl()
