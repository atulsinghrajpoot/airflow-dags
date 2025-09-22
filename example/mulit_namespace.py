from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1)
}
def my_function():
    print("Hello from the Airflow task!")
 
with DAG( dag_id="mulit_namespace",
    default_args=default_args,
    description="A simple sample DAG",
    schedule=timedelta(minutes=5),  # runs every 1 minute
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["example"]) as dag:
    
    task = PythonOperator(
        task_id='run_in_other_namespace',
        python_callable=my_function,
        executor_config={
            "pod_override": {
                "metadata": {"namespace": "cisco"}
            }
        }
    )
