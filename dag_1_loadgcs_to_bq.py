from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
}

# Define the DAG
with DAG(
    'gcs_to_bigquery_load',
    default_args=default_args,
    description='Load Data from GCS to BigQuery',
    schedule_interval=None,  # Set to None for manual triggering
    catchup=False,
) as dag:

    # Task: Load data from GCS to BigQuery
    load_data_to_bq = GCSToBigQueryOperator(
        task_id='load_data_to_bigquery',
        bucket='n-prac-bucket',  # The name of the GCS bucket
        source_objects=['Data.csv'],  # Path to your file(s) in GCS
        destination_project_dataset_table='tt-sandbox-002.n_prac_test_dataset.composer02',  # BigQuery destination (project.dataset.table)
        source_format='CSV',  # The format of the source file(s) in GCS (CSV, JSON, AVRO, etc.)
        skip_leading_rows=1,  # Optional: Skip the header row in the CSV file
        autodetect=True,  # Optional: Let BigQuery autodetect the schema (works well with CSV/JSON)
        write_disposition='WRITE_APPEND',  # What to do if the table already exists. Options: 'WRITE_APPEND', 'WRITE_TRUNCATE', 'WRITE_EMPTY'
        field_delimiter=',',  # Delimiter used in the CSV file
    )

    load_data_to_bq  # This task is standalone, so no task dependencies
