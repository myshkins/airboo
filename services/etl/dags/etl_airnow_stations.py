"""airnow dag for ingesting station data"""
from datetime import datetime as dt
from datetime import timedelta

import pandas as pd
import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator



BASE_URL = "https://s3-us-west-1.amazonaws.com//files.airnowtech.org/airnow/"
yesterday = (dt.now() - timedelta(days=1)).strftime("%Y%m%d")
year = dt.now().year
url = f"{BASE_URL}{year}/{yesterday}/Monitoring_Site_Locations_V2.dat"

@dag(
    dag_id="etl_airnow_stations",
    schedule=timedelta(hours=12),
    start_date=dt(2022, 12, 1, 12, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=5),
)
def etl_airnow_stations():
    """
    Dag definition for pulling airnow station data, shaping that data, and
    putting it into the station table.
    """
    create_temp_station_table = PostgresOperator(
        task_id="create_table_temp_airnow_stations",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_table_temp_airnow_stations.sql",
    )

    @task
    def get_station_data():
        """gets station data file from airnow.org and writes it to .csv"""
        with open('/opt/airflow/dags/files/station_data.csv', mode='w') as file:
            response = requests.get(url)
            file.write(response.text)

    @task
    def shape_station_data():
        """
        reads station data from csv, shapes it with pandas, and loads it to
        temp_airnow_stations
        """
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
        df.to_csv(
            '/opt/airflow/dags/files/station_data.csv',
            sep='|',
            header=False, index=False
            )

        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        hook.copy_expert(
            sql="""
                COPY temp_airnow_stations FROM stdin WITH DELIMITER AS '|' 
                NULL AS ''
                """,
            filename='/opt/airflow/dags/files/station_data.csv')
    

    create_temp_station_table >> get_station_data() >> shape_station_data()

etl_airnow_stations()