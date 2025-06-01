from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.utils.dates import days_ago

# Define bucket names
SOURCE_BUCKET = "sid_bucket_01"
DESTINATION_BUCKET = "siddhesh_csv"
PREFIX = ""  # Move all files, or specify a folder (e.g., "folder/")

# Default arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
}

# Define DAG
with DAG(
    "move_gcs_files",
    default_args=default_args,
    schedule_interval=None,  # Correct way to disable scheduling
    catchup=False
) as dag:

    # Move files from SOURCE_BUCKET to DESTINATION_BUCKET
    move_files = GCSToGCSOperator(
        task_id="move_files_to_new_bucket",
        source_bucket=SOURCE_BUCKET,
        destination_bucket=DESTINATION_BUCKET,
        source_object=PREFIX + "*",
        move_object=True,
    )

    move_files  # Setting task execution
