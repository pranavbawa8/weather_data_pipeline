from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import AwsGlueCrawlerOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import boto3
from datetime import datetime

# Constants
RAW_BUCKET = "raw-bucket"
PROCESSED_BUCKET = "processed-bucket"
REDSHIFT_TABLE = "weather_data"
REDSHIFT_SCHEMA = "public"
GLUE_CRAWLER_NAME = "weather-data-crawler"
GLUE_JOB_NAME = "weather-data-etl-job"

# Initialize S3 client
s3 = boto3.client('s3')

def archive_raw_data(**context):
    # Get the raw data file path (passed as a parameter)
    raw_file_key = context['params'].get('raw_file_key')
    
    # Generate archive path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_key = f"archive/{timestamp}/{raw_file_key.split('/')[-1]}"
    
    # Copy and delete the raw file
    s3.copy_object(
        Bucket=RAW_BUCKET,
        CopySource={"Bucket": RAW_BUCKET, "Key": raw_file_key},
        Key=archive_key
    )
    s3.delete_object(Bucket=RAW_BUCKET, Key=raw_file_key)

def archive_processed_data(**context):
    # Get the processed file path (from Glue Job output)
    processed_file_key = "processed-data/processed_data.parquet"
    
    # Generate archive path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_key = f"archive/{timestamp}/processed_data.parquet"
    
    # Copy and delete the processed file
    s3.copy_object(
        Bucket=PROCESSED_BUCKET,
        CopySource={"Bucket": PROCESSED_BUCKET, "Key": processed_file_key},
        Key=archive_key
    )
    s3.delete_object(Bucket=PROCESSED_BUCKET, Key=processed_file_key)

# Define DAG
with DAG(
    dag_id='data_pipeline_with_archival',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False
) as dag:

    # Task 1: Run Glue Crawler
    run_crawler = AwsGlueCrawlerOperator(
        task_id='run_crawler',
        crawler_name=GLUE_CRAWLER_NAME,
        aws_conn_id='aws_default'
    )

    # Task 2: Run Glue ETL Job
    run_glue_job = AwsGlueJobOperator(
        task_id='run_glue_job',
        job_name=GLUE_JOB_NAME,
        aws_conn_id='aws_default',
        job_args={
            '--input_bucket': RAW_BUCKET,
            '--output_bucket': PROCESSED_BUCKET
        }
    )

    # Task 3: Load data to Redshift
    load_to_redshift = S3ToRedshiftOperator(
        task_id='load_to_redshift',
        schema=REDSHIFT_SCHEMA,
        table=REDSHIFT_TABLE,
        s3_bucket=PROCESSED_BUCKET,
        s3_key='processed-data/',
        aws_conn_id='aws_default',
        redshift_conn_id='redshift_default'
    )

    # Task 4: Archive raw data
    archive_raw = PythonOperator(
        task_id='archive_raw_data',
        python_callable=archive_raw_data,
        provide_context=True,
        op_kwargs={'raw_file_key': 'new-data/raw_weather_data.csv'}  # Pass the file path
    )

    # Task 5: Archive processed data
    archive_processed = PythonOperator(
        task_id='archive_processed_data',
        python_callable=archive_processed_data
    )

    # Define dependencies
    run_crawler >> run_glue_job >> load_to_redshift >> [archive_raw, archive_processed]