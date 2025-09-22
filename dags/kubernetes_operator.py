from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime, timedelta
from kubernetes import client as k8s

# -----------------------------
# Shared Volume (optional, for testing)
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
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["k8s", "dbt"],
):

    dbt_task = KubernetesPodOperator(
        task_id="run_dbt_task",
        name="run-dbt-task",
        namespace="cisco",  # 👈 runs in Cisco namespace
        image="alpine:latest",  # replace with dbt image later
        cmds=["sh", "-c"],
        arguments=["echo 'Running dbt transformation...' && sleep 1000"],
        get_logs=True,
        in_cluster=True,
        # is_delete_operator_pod=True,
        service_account_name="airflow-service-account",  # 👈 must exist with RBAC
        volume_mounts=[generic_shared_volume_mount],
        volumes=[generic_shared_volume],
    )
