import pendulum
from airflow.decorators import dag, task
from api_interface.get_stations import get_waqi_stations
from db.db_engine import engine, get_db
from db.models import Base
from db.models.waqi_stations import WAQI_Stations, WAQI_Stations_Temp
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.schema import CreateTable, DropTable
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
        # with get_db() as db:
        #     DropTable(WAQI_Stations_Temp, bind=engine)
        #     db.flush()
        #     Base.metadata.create_all(engine)
        #     db.flush()
            # CreateTable(WAQI_Stations_Temp, bind=engine)

    @task()
    def get_stations():
        stations = get_waqi_stations()
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


# Base.metadata.create_all(bind=engine)
etl_waqi_stations()