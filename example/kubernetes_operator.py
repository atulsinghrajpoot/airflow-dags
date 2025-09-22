from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime
from kubernetes import client as k8s

# -----------------------------
# Shared Volume (optional)
# -----------------------------
generic_shared_volume = k8s.V1Volume(
    name="shared-temp-volume",
    empty_dir=k8s.V1EmptyDirVolumeSource()
)

generic_shared_volume_mount = k8s.V1VolumeMount(
    name="shared-temp-volume",
    mount_path="/tmp/shared",
    read_only=False
)

# -----------------------------
# DAG Definition
# -----------------------------
default_args = {"owner": "airflow"}

with DAG(
    dag_id="sample_flow",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,  # manual trigger
    catchup=False,
    tags=["k8s", "dbt"],
) as dag:

    dbt_task = KubernetesPodOperator(
        task_id="run_dbt_task",
        name="run-dbt-task",
        namespace="cisco",  # 👈 ensure this is the target namespace
        image="alpine:latest",  # replace with your DBT image
        cmds=["sh", "-c"],
        arguments=[
            "echo 'Running dbt transformation...' && sleep 30"
        ],
        get_logs=True,               # 👈 ensures Airflow streams logs via API
        in_cluster=True,             # 👈 required for k8s cluster access
        is_delete_operator_pod=True, # 👈 cleans up pods after completion
        service_account_name="airflow-service-account",  # 👈 must exist
        volumes=[generic_shared_volume],
        volume_mounts=[generic_shared_volume_mount],
        startup_timeout_seconds=600,
    )
