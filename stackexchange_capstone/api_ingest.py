from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils import timezone
import json
import pandas as pd
import requests
import datetime as dt
import os
import logging
import time

logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)
# can use airflow logging throughout, but use both.

# TODO use airflow secrets? YES
# TODO add oauth flow using requests to retrieve from URL and store access token in AIrflow DB
# https://stackoverflow.com/oauth/dialog?client_id=19164&scope=no_expiry&redirect_uri=https://stackexchange.com
# https://stackoverflow.com/oauth/dialog?client_id=19164&scope=no_expiry&redirect_uri=https://stackexchange.com

# not needed if using implicit
# https://stackoverflow.com/oauth/access_token?client_id=19164&client_secret=v06gKNiEjuMqBE2DercZLQ((&code=L2XssqvPr89YTQmZ3t9ngQ))&redirect_uri=https://stackexchange.com (in postman)


with open(os.path.join(os.getcwd(), '.envs.json')) as f:
    data = json.load(f)
# TODO use airflow secrets, not os.environ
os.environ['alert_email'] = data['alert_email']
os.environ['access_token'] = data['access_token']
os.environ['key'] = data['key']

# TODO docstrings
# TODO logging
# TODO how to structure project in github, given dags should live in ~/airflow/dags?
# TODO check api returned results for hug-of-death loops ie. out of quota


def get_daily_data(obj: str, filter: str):
    """For a given StackExchange API object, call the API to retrieve all records created after 'from_date'. Writes results to local JSON file.
    Args:
        - obj: (str) object type from StackExchange (e.g. Users, Questions)
        - filter: (str) string that is interpreted by the API to select which columns to return for a given object
    Returns:
        - None: writes results of API calls to local JSON file with filename <date>_<obj>.json"""
    page = 1
    # TODO adjust date/time window to ensure data isn't missing or overlapping
    # TODO abstract from_date to argument
    from_date = int(dt.datetime.combine(dt.date.today() -
                                        dt.timedelta(days=1), dt.time()).timestamp())
    has_more = True
    quota_remaining = 1
    data = {}
    backoff = 0
    while has_more and quota_remaining > 0:
        url = 'https://api.stackexchange.com/2.2/'+obj+('/recipients' if obj == 'badges' else '')+'?&fromdate='+str(from_date) \
            + '&page=' + \
            str(page)+'&pagesize=100&site=stackoverflow&filter='+filter+'&key=' + \
            os.environ['key']+'&access_token='+os.environ['access_token']
        # if backoff throttling is encountered, sleep for backoff duration
        time.sleep(int(backoff))
        r = requests.get(url)
        data[page] = r.json()
        page += 1
        has_more = r.json().get('has_more', False)
        quota_remaining = r.json().get('quota_remaining', 0)
        backoff = r.json().get('backoff', 0)
    try:
        dfs = [pd.DataFrame(data[i]['items']) for i in data.keys()]
    except:
        with open(f'./{obj}_data_dump.json', 'w') as f:
            json.dump(data, f)
    df_agg = pd.concat(dfs).reset_index(drop=True)
    #df_agg.to_json(str(dt.date.today())+'_'+str(obj)+'.json', orient='records')

    # TODO is there a better format to write to? Parquet for Spark/Hive?
    path = str(dt.date.today())+'_'+str(obj)+'.parquet'
    df_agg.to_parquet(path)


default_args = {
    "owner": "airflow",
    "start_date": timezone.datetime(2020, 12, 1),
    "email": os.environ.get('alert_email'),
    "email_on_failure": True,
    "retries": 0}
# TODO change schedule_interval to @daily
dag = DAG(dag_id='daily_retrieval', catchup=False,
          schedule_interval='@daily', default_args=default_args)


objs = {'badges': '!*Jxe6CzkgnnrOHSD', 'comments': '!1zSsisQasXo7EZNLWi8Gc', 'users': '!BTSv8IU8MCL.o*1iHmyiJz2RKd47Xm',
        'questions': '!*IXk1kQqzs_F5H7WdeRgFI0Bpw4)*YL67x38l37LYduZdAgzLM5zX(5E3SrjEa', 'answers': '!*cCFgu5yS6u_i7sFIGkyTONJTIFRsBq)FVBsX'}
get_tasks = []

for i, (k, v) in enumerate(objs.items()):
    get_tasks.append(PythonOperator(
        task_id='get_'+k, python_callable=get_daily_data, op_args=[k, v], dag=dag
    ))
    if i != 0:
        get_tasks[i-1] >> get_tasks[i]
