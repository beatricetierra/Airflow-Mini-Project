from datetime import datetime 
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pathlib import Path

def get_logs(*args):
    log_dir = '/opt/airflow/logs/marketvol/' + args[0]
    file_list = Path(log_dir).rglob('*.log')

    for file in file_list:
        print("Analysis for log file: {}".format(file))
        count, cur_list = analyze_file(file)
        if count != 0:
            print('Total number of errors: {}'.format(count))
            print('Here are all the errors:')
            [print(error) for error in cur_list]
        else:
            print('No errors"')

def analyze_file(file):
    count = 0
    cur_list = []

    fp = open(file)
    for line in fp:
        if "ERROR -" in line:
            count+=1
            cur_list.append(line)
    fp.close()
    return count, cur_list

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime.now() - timedelta(days=1)
}

dag_log_analyzer = DAG(
dag_id='loganalyzer',
default_args=default_args,
description='DAG to analyzer marketvol dag logs.'
)

t1 = PythonOperator(
    task_id='analyze_aapl_data',
    python_callable=get_logs,
    op_args = ['download_aapl_data'],
    provide_context=True,
    dag=dag_log_analyzer,
)

t2 = PythonOperator(
    task_id='analyze_tsla_data',
    python_callable=get_logs,
    op_args = ['download_tsla_data'],
    provide_context=True,
    dag=dag_log_analyzer,
)


