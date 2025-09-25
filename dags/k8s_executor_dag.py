from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="two_pods_both_in_cisco",
    start_date=datetime(2025, 9, 19),
    catchup=False,
    schedule=None
) as dag:

    k8s_task = KubernetesPodOperator(
        namespace="cisco",   # the business pod
        image="alpine:3.18",
        cmds=["sh", "-c"],
        arguments=["echo 'Hello from Cisco'; sleep 60"],
        name="hello-cisco",
        task_id="hello_cisco_task",
        get_logs=True,
        is_delete_operator_pod=False,
        executor_config={
            "KubernetesExecutor": {
                "namespace": "cisco"   # the operator’s pod
            }
        }
    )
