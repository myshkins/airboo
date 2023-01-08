import pendulum
from airflow.decorators import dag, task
from api_interface.get_stations import get_waqi_stations
from db.db_engine import get_db
from db.models import Stations_WAQI_Temp
from sqlalchemy import insert
from util.read_sql import read_sql


@dag(
    schedule = "@daily",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup = False,
    tags=["stations"]
)
def etl_waqi_stations():
    """This dag retrieves all stations from the World Air Quality Index project: https://aqicn.org/api/"""

    @task()
    def create_stations_temp():
        sql_stmts = read_sql("dags/sql/create_table_stations_waqi_temp.sql")
        for stmt in sql_stmts:
            with get_db() as db:
                result = db.execute(stmt)
                db.commit()

    @task()
    def get_stations():
        stations = get_waqi_stations()
        return stations


    @task()
    def load_stations_temp(waqi_stations):
        with get_db() as db:
            db.execute(insert(Stations_WAQI_Temp), waqi_stations,)
            db.commit()


    @task()
    def load_stations():
        pass


    task_1 = create_stations_temp()
    task_2 = get_stations()
    task_3 = load_stations_temp(task_2)
    task_1 >> task_2 >> task_3

etl_waqi_stations()