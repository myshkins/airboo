import os
import pendulum
import requests
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from api_interface import get_waqi_data as gwd

# airflow DAG

@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["external_aq_data"],
)
def get_aq_intl_data():
    """
    This dag retrieves data from World Air Quality Index project: https://aqicn.org/api/
    """

    @task
    def extract_waqi_data():
        waqi_data = gwd.get_aq_data()
        return waqi_data


    @task
    def print_waqi_data(aq_data: str):
        return aq_data 

    extracted_data = extract_waqi_data()
    print_waqi_data(extracted_data)

get_aq_intl_data()