import pendulum
from airflow.decorators import dag, task
from api_interface.get_stations_waqi import get_stations_waqi
from db.db_engine import get_db
from shared_models.stations_waqi import Waqi_Stations, Waqi_Stations_Temp
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


@dag(
    schedule="@daily",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["stations"],
)
def etl_stations_waqi():
    """This dag retrieves all stations from the World Air Quality Index
    project: https://aqicn.org/api/"""

    @task()
    def create_stations_temp():
        with get_db() as db:
            engine = db.get_bind()
            if engine.has_table("stations_waqi_temp"):
                Waqi_Stations_Temp.__table__.drop(db.get_bind())
            Waqi_Stations_Temp.__table__.create(db.get_bind())

    @task()
    def get_stations():
        stations = get_stations_waqi()
        return stations

    @task()
    def load_stations_temp(waqi_stations):
        with get_db() as db:
            db.execute(insert(Waqi_Stations_Temp), waqi_stations)
            db.commit()

    @task()
    def load_stations():
        with get_db() as db:
            insert_stmt = insert(Waqi_Stations).from_select(
                (
                    Waqi_Stations.station_id,
                    Waqi_Stations.station_name,
                    Waqi_Stations.latitude,
                    Waqi_Stations.longitude,
                    Waqi_Stations.request_datetime,
                    Waqi_Stations.data_datetime,
                ),
                select(Waqi_Stations_Temp),
            )

            upsert = insert_stmt.on_conflict_do_update(
                index_elements=[Waqi_Stations.station_id],
                set_={
                    Waqi_Stations.station_name: insert_stmt.excluded.station_name,
                    Waqi_Stations.latitude: insert_stmt.excluded.latitude,
                    Waqi_Stations.longitude: insert_stmt.excluded.longitude,
                    # Waqi_Stations.request_datetime:
                    # Waqi_Stations... insert_stmt.excluded.request_datetime,
                    Waqi_Stations.data_datetime: insert_stmt.excluded.data_datetime,
                },
            )
            db.execute(upsert)
            db.commit()

    task_1 = create_stations_temp()
    task_2 = get_stations()
    task_3 = load_stations_temp(task_2)
    task_4 = load_stations()
    task_1 >> task_2 >> task_3 >> task_4


etl_stations_waqi()
