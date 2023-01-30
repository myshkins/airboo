import pendulum
from airflow.decorators import dag, task
from api_interface.get_stations_waqi import get_stations_waqi
from db.db_engine import get_db
from shared_models.stations_waqi import WAQI_Stations, WAQI_Stations_Temp
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from util.util_sql import read_sql, exec_sql


@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["stations"]
)
def etl_stations_waqi():
    """This dag retrieves all stations from the World Air Quality Index
    project: https://aqicn.org/api/"""

    @task()
    def create_stations_temp():
        sql_stmts = read_sql("dags/sql/create_table_stations_waqi_temp.sql")
        exec_sql(sql_stmts)

    @task()
    def get_stations():
        stations = get_stations_waqi()
        return stations

    @task()
    def load_stations_temp(waqi_stations):
        with get_db() as db:
            db.execute(insert(WAQI_Stations_Temp), waqi_stations,)
            db.commit()

    @task()
    def load_stations():
        with get_db() as db:
            insert_stmt = insert(WAQI_Stations).from_select((
                WAQI_Stations.station_id,
                WAQI_Stations.station_name,
                WAQI_Stations.latitude,
                WAQI_Stations.longitude,
                WAQI_Stations.request_datetime,
                WAQI_Stations.data_datetime)
            ,
            select(WAQI_Stations_Temp))

            upsert = insert_stmt.on_conflict_do_update(
                index_elements=[WAQI_Stations.station_id],
                set_ = {
                    WAQI_Stations.station_name: insert_stmt.excluded.station_name,
                    WAQI_Stations.latitude: insert_stmt.excluded.latitude,
                    WAQI_Stations.longitude: insert_stmt.excluded.longitude,
                    WAQI_Stations.request_datetime: insert_stmt.excluded.request_datetime,
                    WAQI_Stations.data_datetime: insert_stmt.excluded.data_datetime
                }
            )
            db.execute(upsert)
            db.commit()

    task_1 = create_stations_temp()
    task_2 = get_stations()
    task_3 = load_stations_temp(task_2)
    task_4 = load_stations()
    task_1 >> task_2 >> task_3 >> task_4

etl_stations_waqi()