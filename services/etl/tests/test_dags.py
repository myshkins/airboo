import os

from airflow.models import DagBag


def test_dags_load_with_no_errors():
    print(os.getcwd())
    dag_bag = DagBag(dag_folder='./services/etl/dags', include_examples=False)
    assert len(dag_bag.import_errors) == 0, f"import errors for {dag_bag.import_errors}"
    assert len(dag_bag.dags) > 1, f"there are less than 1 dags imported: {dag_bag.dagbag_report}"
    # print(f"dag_bag.report = {dag_bag.dagbag_report}")
    # print(f"dag_bag.dags = {dag_bag.dags}")
