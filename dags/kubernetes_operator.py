from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="k8s_operator_example",
    start_date=datetime(2024, 9, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    k8s_task = KubernetesPodOperator(
        namespace="airflow",
        image="python:3.9-slim",
        cmds=["python", "-c"],
        arguments=["print('Hello from KubernetesPodOperator!')"],
        labels={"app": "airflow"},
        name="k8s-operator-task",
        task_id="run_pod_task",
        is_delete_operator_pod=True,   # cleanup after run
        get_logs=True,
    )
