from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator

# =============================================================================
# CONFIGURATION
# =============================================================================
# Change these variables if actual AWS resource names differ.

BRONZE_CRAWLER_NAME = "ai-augmented-bronze-crawler"
BRONZE_TO_SILVER_JOB_NAME = "silvertranform"

SILVER_CRAWLER_NAME = "ai-augmented-silver-crawler"
SILVER_TO_GOLD_JOB_NAME = "silver to gold "

GOLD_CRAWLER_NAME = "ai-augmented-gold-crawler"

AWS_CONN_ID = "aws_default"
REGION_NAME = "eu-north-1"
GLUE_ROLE = "AWSGlueServiceRole-AIAugmentedDataPlatform"

# =============================================================================
# DEFAULT ARGS & DAG DEFINITION
# =============================================================================

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ai_augmented_ecommerce_pipeline",
    description="AWS Medallion Data Pipeline - Bronze to Silver to Gold",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["aws", "glue", "pyspark", "medallion"],
) as dag:

    # -----------------------------------------------------
    # 1. Crawl Bronze data
    # -----------------------------------------------------

    crawl_bronze = GlueCrawlerOperator(
        task_id="crawl_bronze",
        config={
            "Name": BRONZE_CRAWLER_NAME
        },
        aws_conn_id=AWS_CONN_ID,
        region_name=REGION_NAME,
        wait_for_completion=True,
    )

    # -----------------------------------------------------
    # 2. Bronze -> Silver PySpark ETL
    # -----------------------------------------------------

    bronze_to_silver = GlueJobOperator(
        task_id="bronze_to_silver",
        job_name=BRONZE_TO_SILVER_JOB_NAME,
        iam_role_name=GLUE_ROLE,
        aws_conn_id=AWS_CONN_ID,
        region_name=REGION_NAME,
        wait_for_completion=True,
    )

    # -----------------------------------------------------
    # 3. Crawl Silver
    # -----------------------------------------------------

    crawl_silver = GlueCrawlerOperator(
        task_id="crawl_silver",
        config={
            "Name": SILVER_CRAWLER_NAME
        },
        aws_conn_id=AWS_CONN_ID,
        region_name=REGION_NAME,
        wait_for_completion=True,
    )

    # -----------------------------------------------------
    # 4. Silver -> Gold dimensional model
    # -----------------------------------------------------

    silver_to_gold = GlueJobOperator(
        task_id="silver_to_gold",
        job_name=SILVER_TO_GOLD_JOB_NAME,
        iam_role_name=GLUE_ROLE,
        aws_conn_id=AWS_CONN_ID,
        region_name=REGION_NAME,
        wait_for_completion=True,
    )

    # -----------------------------------------------------
    # 5. Crawl Gold
    # -----------------------------------------------------

    crawl_gold = GlueCrawlerOperator(
        task_id="crawl_gold",
        config={
            "Name": GOLD_CRAWLER_NAME
        },
        aws_conn_id=AWS_CONN_ID,
        region_name=REGION_NAME,
        wait_for_completion=True,
    )

    # -----------------------------------------------------
    # PIPELINE DEPENDENCIES
    # -----------------------------------------------------

    (
        crawl_bronze
        >> bronze_to_silver
        >> crawl_silver
        >> silver_to_gold
        >> crawl_gold
    )