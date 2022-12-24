"""airnow etl functions"""
import os
from datetime import timedelta, datetime as dt

from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests
import pandas as pd


yesterday = (dt.now() - timedelta(days=1)).strftime("%Y%m%d")
year = dt.now().year

BASE_URL = "https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow/"

url = f"{BASE_URL}{year}/{yesterday}/Monitoring_Site_Locations_V2.dat"

@dag(
    dag_id="airnow_station_ingest",
    schedule=timedelta(days=1),
    start_date=dt(2022, 12, 1, 12, 00),
    catchup=False,
    dagrun_timeout=timedelta(minutes=5),
)
def airnow_station_ingest():
    """
    Dag definition for pulling airnow station data, shaping that data, and
    putting it into the station table.
    """
    create_temp_station_table = PostgresOperator(
        task_id="create_temp_airnow_station_table",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_temp_airnow_station_table.sql",
    )
    @task
    def get_station_data():
        """gets station data file from airnow.org and writes it to .csv"""
        with open('/opt/airflow/dags/files/station_data.csv', mode='w') as file:
            response = requests.get(url)
            file.write(response.text)

    @task
    def shape_station_data():
        """reads station data from csv and shapes it with pandas"""
        df = pd.read_csv(
            "/opt/airflow/dags/files/station_data.csv", delimiter="|"
        )
        df = df.drop(
            ["StationID","AQSID","FullAQSID","MonitorType","SiteCode",
             "AgencyID", "EPARegion","CBSA_ID","CBSA_Name","StateAQSCode",
             "StateAbbreviation", "Elevation", "GMTOffset", "CountyName",
             "CountyAQSCode"],
            axis=1
        )
        df = df.groupby("CountryFIPS").get_group("US")
        df = df.groupby("Status").get_group("Active")
        df.drop(["Status", "CountryFIPS"], axis=1, inplace=True)
        param_groups = df.groupby("Parameter")
        PM2_5 = param_groups.get_group("PM2.5").drop("Parameter", axis=1)
        PM10 = param_groups.get_group("PM10").drop("Parameter", axis=1)
        df = pd.merge(
            PM10,
            PM2_5,
            how="outer",
            on=["Latitude", "Longitude", "SiteName", "AgencyName"],
        )
        df = df.drop_duplicates(subset="SiteName", keep='first')
        df = df.replace({',': '-'}, regex=True)
        df = df.dropna(axis=0)
        df['Location Coord.'] = list(zip(df["Latitude"], df["Longitude"]))
        df.to_csv('/opt/airflow/dags/files/station_data.csv', sep='|', header=False, index=False)

        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        hook.copy_expert(
            sql="COPY temp_airnow_stations FROM stdin WITH DELIMITER AS '|' NULL AS ''",
            filename='/opt/airflow/dags/files/station_data.csv')

    @task
    def load_station_data():
        """upsert new station data to the production station table"""

        query = """
        INSERT INTO prod_airnow_stations (station_name, agency_name, latitude, longitude, location_coord)
            SELECT * FROM temp_airnow_stations
            ON CONFLICT DO NOTHING
        """
        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        conn = hook.get_conn()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()


    create_temp_station_table >> get_station_data()
    shape_station_data()
    load_station_data()

airnow_station_ingest()