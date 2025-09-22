from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="simple_cisco_dag",
    start_date=datetime(2025, 9, 19),
    catchup=False,
    schedule=None
) as dag:

    k8s_task = KubernetesPodOperator(
        namespace="cisco",           # Pod will run in Cisco namespace
        image="alpine:3.18",         # lightweight container
        cmds=["echo", "Hello from Cisco namespace!"],
        name="hello-cisco",
        task_id="hello_cisco_task",
        get_logs=True
    )
