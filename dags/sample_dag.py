from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default args for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define DAG
with DAG(
    dag_id="sample_dag",
    default_args=default_args,
    description="A simple sample DAG",
    schedule=timedelta(minutes=1),  # runs every 1 minute
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:



    task1 = BashOperator(
        task_id="print_date",
        bash_command="date"
    )

    task2 = BashOperator(
        task_id="say_hello",
        bash_command="echo 'Hello from Airflow DAG!'"
    )

    task1 >> task2
