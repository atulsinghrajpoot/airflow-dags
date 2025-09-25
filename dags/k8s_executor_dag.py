from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="k8s_executor_dag",
    start_date=datetime(2025, 9, 19),
    catchup=False,
    schedule=None
) as dag:
    task = BashOperator(
        task_id="hello_cisco_task",
        bash_command="echo 'Hello from Cisco'; sleep 60",
        executor_config={
            "KubernetesExecutor": {
                "namespace": "cisco"
            }
        }
    )
