# from datetime import timedelta

# import pendulum
# import pytest
# from airflow import DAG


# @pytest.fixture
# def test_dag():
#     return DAG(
#         "test_dag",
#         default_args={
#             "owner": "airflow",
#             "start_date": pendulum.datetime(2023, 1, 1, tz="UTC")
#         },
#         schedule_interval=timedelta(days=1),
#     )


# @pytest.helpers.register
# def run_task(task, dag):
#     dag.clear()
#     dag.test()
#     # task.test(
#     #     start_date=dag.default_args["start_date"],
#     #     end_date=dag.default_args["end_date"],
#     # )
