# python_operator_test.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from kubernetes.client import V1Pod, V1ObjectMeta  # import required classes

with DAG(
    dag_id="python_operator_test",
    default_args=default_args,
    description="A simple sample DAG",
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    task2 = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow DAG!'; sleep 60",
        executor_config={
            "pod_override": V1Pod(
                metadata=V1ObjectMeta(namespace="cisco")
            )
        }
    )
