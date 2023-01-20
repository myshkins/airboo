import pendulum
from airflow.decorators import dag, task
from api_interface import get_waqi_data as gwd
from db.db_engine import get_db
from db.models.waqi_readings import Readings_WAQI_Temp
from util.read_sql import read_sql


@dag(
    schedule=pendulum.duration(minutes=1),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=["readings"],
)
def etl_readings_waqi():
    """
    This dag retrieves air quality readings data from World Air Quality Index project: https://aqicn.org/api/
    """
        
    @task()
    def create_temp_waqi():
        sql_stmts = read_sql('dags/sql/create_table_readings_waqi_temp.sql')
        for stmt in sql_stmts:
            with get_db() as db:
                result = db.execute(stmt)
                db.commit()

    @task()
    def get_readings_waqi():
        waqi_data = gwd.get_waqi_data()
        return waqi_data

    @task()
    def load_readings_waqi_temp(waqi_data):
       new_row = Readings_WAQI_Temp(**waqi_data)
       with get_db() as db:
            result = db.add(new_row)
            db.commit()
            db.refresh(new_row)
            
    @task()
    def load_readings_waqi():
        sql_stmts = read_sql('dags/sql/load_readings_waqi.sql')
        for stmt in sql_stmts:
            with get_db() as db:
                result = db.execute(stmt)
                db.commit()

    task_1 = create_temp_waqi()
    task_2 = get_readings_waqi()
    task_3 = load_readings_waqi_temp(task_2)
    task_4 = load_readings_waqi()

    task_1 >> task_2 >> task_3 >> task_4

etl_readings_waqi()