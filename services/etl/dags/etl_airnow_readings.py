"""
airnow etl functions

for initial setup:
    1. run etl_airnow_stations dag
    2. run etl_airnow dag (the dag in this file)
    3. at some-hr:59 run load_prod_airnow_stations dag
"""
import os

import numpy as np
import pandas as pd
import pendulum
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from config import Settings
from api_interface import get_airnow_data as gad


@dag(
    dag_id="etl_airnow",
    schedule=pendulum.duration(minutes=10),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=pendulum.duration(minutes=2),
)
def airnow_etl():
    """
    This dag retrieves air quality data from airnow.org for all of USA for
    current hour."""
    
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
        csv_data = gad.get_airnow_data()
        with open(data_path, 'w') as file:
            file.write(csv_data)

    def reshape_airnow_data(df):
        """
        Uses .groupby() to split 'parameter' column into pm2.5 and pm10 groups.
        Then merge groups together under columns:
        site name | datetime | PM10 conc. | PM10 AQI | PM10 AQI cat. |
        PM2_5 conc. | PM2_5 AQI | PM2_5 AQI cat.
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


    a = create_temp_airnow_table 
    b = extract_current_data()
    c = load_to_temp()
    d = load_to_temp()
    e = drop_CA_rows
    f = load_to_production

    a >> b >> c >> d >> e >> f 


dag = airnow_etl()
