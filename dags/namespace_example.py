from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1)
}

with DAG('namespace_example', default_args=default_args, schedule_interval='@daily') as dag:
    task = PythonOperator(
        task_id='run_in_other_namespace',
        python_callable=my_function,
        executor_config={
            "KubernetesExecutor": {
                "namespace": "cisco"  # Specify your target namespace here
            }
        }
    )
