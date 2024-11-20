import os
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests
import configparser

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/opt/airflow/dags/cloudfunction.json'
request = google.auth.transport.requests.Request()

config = configparser.ConfigParser()
config.read('/opt/airflow/dags/configuration.properties')
run_url = config['Cloud Functions']['nytimes']
clean_url = config['Cloud Functions']['cleaning']
keyword_url = config['Cloud Functions']['keyword']
loading_url = config['Cloud Functions']['loading']


ny_timess_rss = {
    "task_world":["https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "world", "nytimes/nytimes-world.csv"],
    "task_us":["https://rss.nytimes.com/services/xml/rss/nyt/US.xml", "us", "nytimes/nytimes-us.csv"],
    "task_europe":["https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml", "europe", "nytimes/nytimes-europe.csv"],
    "task_education":["https://rss.nytimes.com/services/xml/rss/nyt/Education.xml", "education", "nytimes/nytimes-education.csv"],
    "task_economy":["https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml", "economy", "nytimes/nytimes-economy.csv"],
    "task_technology":["https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "technology", "nytimes/nytimes-technology.csv"],
    "task_sports":["https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml", "sports", "nytimes/nytimes-sports.csv"],
    "task_baseball":["https://rss.nytimes.com/services/xml/rss/nyt/Baseball.xml", "baseball", "nytimes/nytimes-baseball.csv"],
    "task_football":["https://rss.nytimes.com/services/xml/rss/nyt/Soccer.xml", "football", "nytimes/nytimes-football.csv"],
    "task_tennis":["https://rss.nytimes.com/services/xml/rss/nyt/Tennis.xml", "tennis", "nytimes/nytimes-tennis.csv"],
    "task_health":["https://rss.nytimes.com/services/xml/rss/nyt/Health.xml", "health", "nytimes/nytimes-health.csv"],
    "task_environment":["https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml", "environment", "nytimes/nytimes-environment.csv"],
    "task_travel":["https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml", "travel", "nytimes/nytimes-travel.csv"],
    "task_golf":["https://rss.nytimes.com/services/xml/rss/nyt/Golf.xml", "golf", "nytimes/nytimes-golf.csv"],
    "task_politics":["https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "politics", "nytimes/nytimes-politics.csv"],
    "task_middleeast":["https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml", "middleeast", "nytimes/nytimes-middleeast.csv"],
    "task_job":["https://rss.nytimes.com/services/xml/rss/nyt/Jobs.xml", "job", "nytimes/nytimes-job.csv"],
}

def call_cloudFunction(base_url, category, file_name, **kwargs):
    TOKEN = google.oauth2.id_token.fetch_id_token(request, run_url)
    r = requests.post(
        run_url, 
        headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
        data=json.dumps({"base_url": base_url, 'category': category, 'file_name': file_name})
    )
    if r.status_code != 200:
        Exception("The Site can not be loaded")
    status, reason, args = r.text.split(" | ")
    if status == "Fail":
        Exception("reason")
    if "No New Data" in reason:
        kwargs['ti'].xcom_push(key='newdata_status', value=False)
    kwargs['ti'].xcom_push(key='newdata_status', value=True)

def call_cloudFunction_clean(prev_task, file_name, **kwargs):
    pulled_value = kwargs['ti'].xcom_pull(dag_id='dag_nytimes', task_ids=prev_task, key='newdata_status')
    if pulled_value == False:
        kwargs['ti'].xcom_push(key='news_clean', value=False)
        return
    TOKEN = google.oauth2.id_token.fetch_id_token(request, clean_url)
    r = requests.post(
        clean_url, 
        headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
        data=json.dumps({'file_name': file_name})
    )
    if r.status_code != 200:
        Exception("The Site can not be loaded")
    status = r.text
    if status == "Fail":
        Exception("Fail")
    kwargs['ti'].xcom_push(key='news_clean', value=True)

def call_cloudFunction_keyword(prev_task, file_name, **kwargs):
    pulled_value = kwargs['ti'].xcom_pull(dag_id='dag_nytimes', task_ids=prev_task, key='news_clean')
    if pulled_value == False:
        kwargs['ti'].xcom_push(key='news_keyword', value=False)
        return
    TOKEN = google.oauth2.id_token.fetch_id_token(request, keyword_url)
    r = requests.post(
        keyword_url, 
        headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
        data=json.dumps({'file_name': file_name})
    )
    if r.status_code != 200:
        Exception("The Site can not be loaded")
    status = r.text
    if status == "Fail":
        Exception("Fail")
    kwargs['ti'].xcom_push(key='news_keyword', value=True)

def call_cloudFunction_load(prev_task, file_name, **kwargs):
    pulled_value = kwargs['ti'].xcom_pull(dag_id='dag_nytimes', task_ids=prev_task, key='news_keyword')
    if pulled_value == False:
        kwargs['ti'].xcom_push(key='news_load', value=False)
        return
    TOKEN = google.oauth2.id_token.fetch_id_token(request, loading_url)
    r = requests.post(
        loading_url, 
        headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
        data=json.dumps({'file_name': file_name})
    )
    if r.status_code != 200:
        Exception("The Site can not be loaded")
    status = r.text
    if status == "Fail":
        Exception("Fail")
    kwargs['ti'].xcom_push(key='news_load', value=True)

dag = DAG(
    dag_id="dag_nytimes",
    schedule_interval='*/15 * * * *',
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    max_active_runs=20
)

# Define tasks
start_task = DummyOperator(task_id='start', dag=dag)
end_task = DummyOperator(task_id='end', dag=dag)

# Define parallel tasks
parallel_tasks_extract = []
parallel_tasks_clean = []
parallel_tasks_keyword = []
parallel_tasks_load = []

for key, values in ny_timess_rss.items():
    parallel_task_extract = PythonOperator(
        task_id=key + "_extract",
        python_callable=call_cloudFunction,
        dag=dag,
        provide_context=True,
        op_args=values
    )
    
    parallel_task_clean = PythonOperator(
        task_id=key + "_clean",
        python_callable=call_cloudFunction_clean,
        dag=dag,
        provide_context=True,
        op_args=[key + "_extract", values[2]]
    )
    
    parallel_task_keyword = PythonOperator(
        task_id=key + "_keyword",
        python_callable=call_cloudFunction_keyword,
        dag=dag,
        provide_context=True,
        op_args=[key + "_clean", values[2]]
    )
    
    parallel_task_load = PythonOperator(
        task_id=key + "_load",
        python_callable=call_cloudFunction_load,
        dag=dag,
        provide_context=True,
        op_args=[key + "_keyword", values[2]]
    )
    
    parallel_tasks_extract.append(parallel_task_extract)
    parallel_tasks_clean.append(parallel_task_clean)
    parallel_tasks_keyword.append(parallel_task_keyword)
    parallel_tasks_load.append(parallel_task_load)

for i in range(len(parallel_tasks_extract)):
    parallel_tasks_extract[i] >> parallel_tasks_clean[i] >> parallel_tasks_keyword[i] >> parallel_tasks_load[i]

start_task >> parallel_tasks_extract
parallel_tasks_load >> end_task