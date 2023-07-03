from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
    'retries': 0
}

dag = DAG(
    'spark_read_csv_write_parquet_fts',
    default_args=default_args,
    schedule_interval=None,
    tags=['e2e example', 'ezaf', 'spark', 'csv', 'parquet', 'fts'],
    params={
        'username': "hpedemo-user01",
        'training_path': "financial-processed",
        's3_secret_name': "spark-s3-creds"
    }
)

submit = SparkKubernetesOperator(
    task_id='submit',
    namespace="spark",
    application_file="example_ezaf_spark_csv_to_parquet_fts.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True
)
