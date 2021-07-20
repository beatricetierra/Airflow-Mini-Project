from datetime import datetime 
from datetime import date
from datetime import timedelta
import pandas as pd
import yfinance as yf

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

def download_AAPL_data():
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    aapl_df = yf.download('AAPL', start=start_date, end=end_date, interval='1m' )
    aapl_df.to_csv('/tmp/data/' + str(start_date) + "/aapl_data.csv", header=False)

def download_TSLA_data():
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    tsla_df = yf.download('TSLA', start=start_date, end=end_date, interval='1d' )
    tsla_df.to_csv('/tmp/data/' + str(start_date) + "tsla_data.csv", header=False)

def query_data(*args):
    filepath = args[0]
    df = pd.read_csv(filepath, header=None)
    timestamp = df[0]
    avg_price = (df[1]+df[2]+df[3]+df[4]+df[5])/5
    result = pd.DataFrame(data={'Timestamp':[timestamp], 'Avg Price':[avg_price]})
    df.to_csv('/opt/airflow/dags/mini-project/History.csv', mode='a', header=False)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['beatricetierra@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime.now(),
    'schedule_interval': '0 18 * * 1-5'
}

dag_yahoo_finance = DAG(
dag_id='marketvol',
default_args=default_args,
description='A simple DAG'
)

t0 = BashOperator(
    task_id='create_tmp_folder',
    bash_command='mkdir -p /tmp/data/$(date +%Y-%m-%d)',
    dag=dag_yahoo_finance
)

t1 = PythonOperator(
    task_id='download_aapl_data',
    python_callable=download_AAPL_data,
    provide_context=True,
    dag=dag_yahoo_finance,
)

t2 = PythonOperator(
    task_id='download_tsla_data',
    python_callable=download_TSLA_data,
    provide_context=True,
    dag=dag_yahoo_finance,
)

t3 = BashOperator(
    task_id='move_appl_data',
    bash_command='mv /tmp/data/$(date +%Y-%m-%d)/aapl_data.csv /opt/airflow/dags/mini-project/output',
    dag=dag_yahoo_finance
)

t4 = BashOperator(
    task_id='move_tsla_data',
    bash_command='mv /tmp/data/$(date +%Y-%m-%d)/tsla_data.csv /opt/airflow/dags/mini-project/output',
    dag=dag_yahoo_finance
)

t5 = PythonOperator(
    task_id='query_data',
    python_callable=query_data,
    op_args=['/opt/airflow/dags/mini-project/output/aapl_data.csv',
    '/opt/airflow/dags/mini-project/output/tsla_data.csv'],
    provide_context=True,
    dag=dag_yahoo_finance
)

t0 >> t1 >> t3 
t0 >> t2 >> t4 
t5.set_upstream(t3)
t5.set_upstream(t4)