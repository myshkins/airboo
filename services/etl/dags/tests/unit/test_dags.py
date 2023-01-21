from airflow.models import DagBag


def test_no_import_errors():
    # dag_folder = '/home/huck/dev/python-projects/air-quality/services/etl/dags'
    dag_bag = DagBag(dag_folder='/home/huck/dev/python-projects/air-quality/services/etl/dags', include_examples=False)
    print(f"DAG BAG = {dag_bag.dagbag_report()}")
    assert len(dag_bag.import_errors) == 0, "No Import Failures"


test_no_import_errors()
