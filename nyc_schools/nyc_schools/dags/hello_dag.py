# /dags/hello_dag.py
from datetime import datetime,timedelta
from airflow import DAG
import requests
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook


def retrieve_venues():
    rds_hook = PostgresHook('rds')
    vals = rds_hook.get_records("""SELECT * FROM venues LIMIT 5;""")
    return vals

def retrieve_categories():
    rds_hook = PostgresHook('rds')
    vals = rds_hook.get_records("""SELECT * FROM categories LIMIT 3;""")
    return vals

 
get_foursquare_info = DAG(dag_id = 'retrieve_foursquare_data', 
                          start_date = datetime.now() - timedelta(days = 1))
 
 
get_venues = PythonOperator(task_id='get_venues', 
                            dag = get_foursquare_info,
                            python_callable = retrieve_venues)

get_categories = PythonOperator(task_id='get_categories', 
                            dag = get_foursquare_info,
                            python_callable = retrieve_categories)


get_venues >> get_categories
# select_states = PostgresOperator(
#         task_id="select_states",
#         postgres_conn_id="rds",
#         sql="""SELECT * FROM states;""", 
#         dag = get_foursquare_info
# )

