from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from ETL import main
import pendulum

# Define the start date as tomorrow at 8:00 AM PST
start_date = datetime(2024, 3, 9, 8, 0, 0, tzinfo=pendulum.timezone('America/Los_Angeles'))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': start_date,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_etl',
    default_args=default_args,
    description='ETL daily',
    schedule_interval='0 8 * * *',  # Run at 8:00 AM PST every day
)

run_etl = PythonOperator(
    task_id='run_etl',
    python_callable=main,
    dag=dag,
)
