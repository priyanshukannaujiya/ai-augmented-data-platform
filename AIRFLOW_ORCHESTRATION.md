# Apache Airflow Orchestration for AWS Glue

This document explains the Apache Airflow setup implemented to orchestrate the AWS Glue Data Pipeline. It serves as both a technical reference and a guide for discussing the architecture during interviews.

## 1. Overview
The platform uses **Apache Airflow** (running locally via Docker) to orchestrate a Medallion Architecture data pipeline on AWS. 

We moved from isolated AWS Glue jobs to an Airflow-orchestrated pipeline to achieve:
- **Centralized Monitoring**: A single pane of glass to view the entire data pipeline's health.
- **Dependency Management**: Guaranteeing that Bronze data is fully crawled and processed before Silver/Gold jobs are executed.
- **Retry Logic & Fault Tolerance**: Automated retries and failure alerts.

## 2. DAG Workflow (The Pipeline)
The DAG (`ai_augmented_ecommerce_pipeline`) manages the end-to-end data processing workflow strictly enforcing dependencies:

1. **`crawl_bronze`**: Uses `GlueCrawlerOperator` to crawl raw data ingested by Kafka into the S3 Bronze bucket.
2. **`bronze_to_silver`**: Uses `GlueJobOperator` to run the PySpark ETL job, validating and casting schema types, saving to Parquet.
3. **`crawl_silver`**: Crawls the newly processed Silver Parquet data.
4. **`silver_to_gold`**: Runs the PySpark job to aggregate Silver data into a Dimensional Model (Star Schema) in the Gold S3 bucket.
5. **`crawl_gold`**: Crawls the Gold data, making `dim_customer`, `dim_product`, `dim_date`, and `fact_orders` queryable via Amazon Athena.

*Dependencies:*
`crawl_bronze >> bronze_to_silver >> crawl_silver >> silver_to_gold >> crawl_gold`

## 3. Infrastructure & Docker Setup
To avoid polluting the host machine's Python environment, Airflow is containerized.

- **Base Image**: `apache/airflow:2.9.2` (Stable official image).
- **Customizations**: A custom `Dockerfile` installs `apache-airflow-providers-amazon` to enable native AWS Operators.
- **Execution**: Uses `SequentialExecutor` with an SQLite backend. This is an intentional choice to keep the local development environment lightweight, as the current pipeline is strictly sequential and does not require parallel task execution (like `CeleryExecutor` with PostgreSQL/Redis).

## 4. Security & Authentication Design
Handling AWS credentials securely in local Docker environments is critical.

- **No Hardcoded Secrets**: AWS Access Keys are **never** hardcoded in Python scripts, `.env` files, or Dockerfiles.
- **Volume Mounting**: The local AWS profile (`~/.aws`) is mounted as a **read-only** volume (`ro`) into the Airflow container at `/opt/airflow/.aws`.
- **Boto3 Integration**: The container environment variables (`AWS_SHARED_CREDENTIALS_FILE`, `AWS_CONFIG_FILE`, `AWS_DEFAULT_REGION`) point to the mounted credentials. Airflow's Amazon provider natively detects and assumes this profile without requiring explicit IAM access key configurations inside the Airflow UI.
- **Git Security**: Strict `.gitignore` rules prevent accidental commits of `.aws/`, `.pem`, `.env`, and local `.db` files.

## 5. Local Execution Guide
To run this project locally, ensure **Docker Desktop is running**, then execute:

```powershell
# 1. Navigate to the airflow directory
cd airflow

# 2. Build the Docker image (installs the AWS provider)
docker compose build

# 3. Start Airflow in the background
docker compose up -d
```
- **Access UI**: `http://localhost:8080`
- **Credentials**: `admin` / `admin`
- **Shutdown**: `docker compose down`

---

## 💡 Interview Talking Points (Why We Built It This Way)

If asked about this implementation during an interview, highlight these technical decisions:

### Q: Why use Apache Airflow instead of AWS Step Functions or EventBridge?
**Answer**: While Step Functions are great for AWS-native serverless orchestration, Airflow provides a vendor-agnostic layer. If we ever wanted to add a Snowflake transformation step (via dbt) or a local data quality check using Great Expectations, Airflow can orchestrate across multiple platforms (AWS, GCP, Snowflake, Local) natively. Furthermore, Airflow's UI provides superior observability for data pipelines out of the box.

### Q: Why use `wait_for_completion=True` on the Operators?
**Answer**: By default, some AWS API calls are asynchronous (fire-and-forget). If we didn't wait for completion, Airflow would instantly mark `bronze_to_silver` as successful the moment the job *started* on AWS, moving on to `crawl_silver` before the data even existed! Enforcing `wait_for_completion=True` ensures the Airflow worker polls the AWS Glue API for the job's terminal status before continuing to the downstream task.

### Q: How do you handle local Docker AWS Authentication?
**Answer**: Security is paramount. Instead of baking AWS keys into a `.env` file (which is risky if accidentally committed), I utilized Docker volume binding to mount my host machine's `~/.aws` directory into the container in a read-only state. This means my container assumes my host's IAM identity dynamically, strictly following the principle of least privilege without duplicating credential files.

### Q: Why use `SequentialExecutor` over `LocalExecutor` or `CeleryExecutor`?
**Answer**: In a production environment (like AWS MWAA), we use CeleryExecutor with a Redis broker and PostgreSQL metadata database to scale workers horizontally. However, for local development of a strictly sequential DAG, standing up Redis and Postgres adds unnecessary overhead and memory consumption to the host machine. The `SequentialExecutor` with SQLite keeps the local demo incredibly lightweight and fast while accurately representing the pipeline logic.
