from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime, timedelta

def read_db_write_csv():
    import mysql.connector
    import pandas as pd
    # Connect to MySQL (running at localhost:3306) and read data
    conn = mysql.connector.connect(
        host='localhost', user='root', password='root', database='PR_JOS'
    )
    df = pd.read_sql('SELECT * FROM some_table', conn)
    conn.close()
    # Write DataFrame to CSV
    df.to_csv('/tmp/output.csv', index=False)

with DAG(dag_id='example_read_write', 
         start_date=datetime(2025,9,19), 
         catchup=False, 
         schedule=timedelta(minutes=5)) as dag:
    # Python task: read from MySQL and write CSV
    read_task = PythonOperator(
        task_id='read_and_write_csv',
        python_callable=read_db_write_csv
    )

    # KubernetesPodOperator: runs in the 'cisco-system' namespace
    k8s_task = KubernetesPodOperator(
        namespace='cisco-system',                    # target namespace for the pod
        image='python:3.8-slim',
        cmds=["bash", "-cx"],
        arguments=["echo Running in Cisco namespace; sleep 10"],
        name='print-namespace',
        task_id='run_in_cisco_ns',
        get_logs=True
    )

    read_task >> k8s_task
