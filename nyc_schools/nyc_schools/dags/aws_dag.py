from datetime import datetime,timedelta
from airflow import DAG
import requests
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.providers.amazon.aws.hooks.ec2 import EC2Hook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
import io
import csv
import os

#used key_id and secret key in 'extra' to fix redshift connection


#docker operator for ec2?

def load_to_s3():
    rds_hook = PostgresHook('rds')
    s3_hook = S3Hook('s3_connection')
    zipcode_records = rds_hook.get_records("SELECT * FROM zipcodes;")
    # create an in memory file
    mem_file = io.StringIO()
    csv_writer = csv.writer(mem_file, lineterminator=os.linesep)
    csv_writer.writerows(zipcode_records)
    # encode into a byte stream
    mem_file_binary = io.BytesIO(mem_file.getvalue().encode())
    s3_hook.load_file_obj(
       file_obj=mem_file_binary,
       bucket_name='jigsaw-bucket',
       key='sample_zipcodes.csv',
       replace=True,
   )

def load_data_to_redshift(*args, **kwargs):
    
    pg_hook = PostgresHook('redshift')
    sql = """COPY sample_zipcodes (id, code, city_id) from 's3://jigsaw-bucket/sample_zipcodes.csv'
        credentials 'aws_iam_role=arn:aws:iam::053194583867:role/redshift_role'
        delimiter ','
        IGNOREHEADER 1
        region 'us-east-1';
        """
    records = pg_hook.run(sql)
    return records


def process_query(**kwargs):
    conn_id = kwargs.get('conn_id')
    pg_hook = PostgresHook(conn_id)
    sql = "Select * FROM sample_zipcodes;"
    records = pg_hook.get_records(sql)
    return records

aws_etl_pipeline = DAG(dag_id = 'aws_etl_pipeline', 
                          start_date = datetime.now() - timedelta(days = 1))


rds_to_s3 = PythonOperator(task_id='rds_to_s3',
                            dag = aws_etl_pipeline,
                            python_callable = load_to_s3)

load_from_s3_to_redshift = PythonOperator(
    task_id='copy_from_s3_to_redshift',
    python_callable= load_data_to_redshift,
    dag=aws_etl_pipeline)

query_redshift = PythonOperator(
    task_id='query_redshift',
    op_kwargs = {'conn_id':'redshift'},
    python_callable=process_query,
    dag=aws_etl_pipeline)

rds_to_s3 >> load_from_s3_to_redshift >> query_redshift

    
