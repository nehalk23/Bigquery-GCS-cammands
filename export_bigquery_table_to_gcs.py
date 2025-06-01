from airflow import DAG
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator
from datetime import datetime

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

# Define the DAG
with DAG(
    dag_id="export_bigquery_table_to_gcs",
    default_args=default_args,
    description="Export BigQuery table to GCS for backup",
    schedule_interval=None,  # None means manual execution
    start_date=datetime(2025, 1, 1),  # Fixed the missing month value
    catchup=False,
) as dag:

    # Task: Export BigQuery table to GCS
    export_bq_to_gcs = BigQueryToGCSOperator(
        task_id="export_bq_to_gcs_task",
        source_project_dataset_table="tt-sandbox-001.siddhesh.n_emp",  # Replace with actual BigQuery table
        destination_cloud_storage_uris=["gs://sid_bucket_01/exported_data_n_emp_{{ ds_nodash }}.csv"],  # Fixed parameter
        export_format="CSV",  
        field_delimiter=",",  
        print_header=True,  
    )

    export_bq_to_gcs  # Register the task
