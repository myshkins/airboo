"""airnow dag for ingesting station data"""
from datetime import timedelta

import pandas as pd
import pendulum
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from api_interface import get_readings_airnow as gad


@dag(
    dag_id="etl_stations_airnow",
    schedule=timedelta(hours=12),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=pendulum.duration(minutes=5),
)
def etl_stations_airnow():
    """
    Dag definition for pulling airnow station data, shaping that data, and
    putting it into the station table.
    """
    create_table_stations_airnow_temp = PostgresOperator(
        task_id="create_table_stations_airnow_temp",
        postgres_conn_id="postgres_etl_conn",
        sql="sql/create_table_stations_airnow_temp.sql",
    )

    @task
    def get_stations_airnow():
        """gets station data file from airnow.org and writes it to .csv"""
        with open('/opt/airflow/dags/files/stations_airnow.csv', mode='w') as file:
            data = gad.get_stations_airnow()
            file.write(data)

    @task
    def shape_station_data():
        """
        reads station data from csv, shapes it with pandas, and loads it to
        stations_airnow_temp
        """
        df = pd.read_csv(
            "/opt/airflow/dags/files/stations_airnow.csv", delimiter="|"
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
            '/opt/airflow/dags/files/stations_airnow.csv',
            sep='|',
            header=False, index=False
            )

        hook = PostgresHook(postgres_conn_id='postgres_etl_conn')
        hook.copy_expert(
            sql="""
                COPY stations_airnow_temp FROM stdin WITH DELIMITER AS '|' 
                NULL AS ''
                """,
            filename='/opt/airflow/dags/files/stations_airnow.csv')

    a = create_table_stations_airnow_temp
    b = get_stations_airnow()
    c = shape_station_data()

    a >> b >> c

etl_stations_airnow()