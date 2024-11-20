import os
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests
import google.oauth2.id_token
import google.auth.transport.requests
import configparser

config = configparser.ConfigParser()
config.read('/opt/airflow/dags/configuration.properties')
run_url = config['Cloud Functions']['notification']

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/opt/airflow/dags/cloudfunction.json'
request = google.auth.transport.requests.Request()

def call_cloudFunction():
    TOKEN = google.oauth2.id_token.fetch_id_token(request, run_url)
    r = requests.post(
        run_url, 
        headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"}
    )
    if r.status_code != 200:
        Exception("The Site can not be loaded")
    
# Define default arguments for the DAG
dag = DAG(
    dag_id="dag_kafka",
    schedule_interval='*/15 * * * *',
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    max_active_runs=10
)

# Define tasks
start_task = DummyOperator(task_id='start_task', dag=dag)

python_task = PythonOperator(
    task_id='send_notification',
    python_callable=call_cloudFunction,
    dag=dag,
)

end_task = DummyOperator(task_id='end_task', dag=dag)

# Define task dependencies
start_task >> python_task >> end_task