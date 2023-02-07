from datetime import timedelta

import pendulum
from airflow.decorators import dag, task
from db.db_engine import get_db
from shared_models.readings_waqi import Readings_Waqi_Temp
from sqlalchemy import insert


@dag(
    schedule=timedelta(minutes=15),
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=["readings"],
)
def etl_readings_waqi():
    """
    This dag retrieves air quality readings data from World Air Quality Index 
    project: https://aqicn.org/api/
    """
    import asyncio

    from api_interface.get_readings_waqi import get_waqi_readings
    from util.util_sql import exec_sql, read_sql

    @task()
    def create_temp_waqi():
        with get_db() as db:
            engine = db.get_bind()
            if engine.has_table('readings_waqi_temp'):
                Readings_Waqi_Temp.__table__.drop(db.get_bind())
            Readings_Waqi_Temp.__table__.create(db.get_bind())

    @task()
    def request_waqi_readings():
        waqi_readings = asyncio.run(get_waqi_readings())
        return waqi_readings

    @task()
    def load_readings_waqi_temp(waqi_data):
        with get_db() as db:
            db.execute(insert(Readings_Waqi_Temp), waqi_data)
            db.commit()

    @task()
    def load_readings_waqi():
        sql_stmts = read_sql('dags/sql/load_readings_waqi.sql')
        exec_sql(sql_stmts)

    task_1 = create_temp_waqi()
    task_2 = request_waqi_readings()
    task_3 = load_readings_waqi_temp(task_2)
    task_4 = load_readings_waqi()

    task_1 >> task_2 >> task_3 >> task_4


etl_readings_waqi()
