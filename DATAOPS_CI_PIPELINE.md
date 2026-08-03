# DataOps CI Pipeline - Interview Preparation Guide

This document outlines the Continuous Integration (CI) and DataOps pipeline implemented via GitHub Actions for the AI-Augmented E-Commerce Data Platform. It serves as a guide for understanding the pipeline's purpose, design, and security mechanisms, especially for technical interviews.

## 1. Objective and Architecture Separation

The project maintains a strict separation of concerns between code validation and runtime execution:

- **GitHub Actions (CI / DataOps):** Responsible for statically validating data engineering code *before* it is merged or deployed. It ensures code health, structural integrity, and security without touching the cloud environment.
- **Apache Airflow (Orchestration):** Responsible for the actual runtime data pipeline. It triggers AWS Glue jobs, Crawlers, and handles data movement (Bronze → Silver → Gold).

**Expected Architecture Flow:**
```mermaid
graph TD
    A[Developer (VS Code)] -->|Git Push| B(GitHub)
    B --> C{GitHub Actions CI}
    C -->|1. Python Syntax| D[Check]
    C -->|2. Structure| E[Check]
    C -->|3. Critical Linting| F[Check]
    C -->|4. Secret Detection| G[Check]
    D --> H[CI PASS]
    E --> H
    F --> H
    G --> H
```

## 2. Pipeline Workflow Steps Explained

The workflow is triggered automatically on any `push` or `pull_request` to the `main` branch. It runs on a lightweight `ubuntu-latest` runner using Python 3.11.

### Step 1: Checkout & Setup
- **Checkout Code (`actions/checkout@v4`):** Clones the repository securely into the GitHub Actions runner environment.
- **Setup Python 3.11 (`actions/setup-python@v5`):** Configures the exact Python version to maintain parity with the development and production environments.

### Step 2: Python Syntax Validation
- **Command:** `python -m compileall . -q`
- **Purpose:** Compiles all Python files to bytecode. If there is a fundamental syntax error anywhere in the repository, the pipeline fails immediately before running heavier checks.

### Step 3: Project Structure Validation
- **Purpose:** Prevents accidental deletion, renaming, or moving of mission-critical data engineering files.
- **Validation:** Verifies the physical presence of:
  - `generator/producer.py`
  - `generator/consumer.py`
  - `airflow/dags/ecommerce_pipeline.py`
- **Interview Talking Point:** "Data pipelines are brittle if dependencies go missing. This step guarantees our core ETL scripts and orchestrator DAGs are always present in the correct paths."

### Step 4: Critical Linting
- **Command:** `flake8 ... --select=E9,F63,F7,F82`
- **Purpose:** Targets high-value Python checks on the critical pipeline files without failing on subjective cosmetic formatting.
- **Errors Caught:** Undefined names (`F82`), invalid syntax (`E9`), invalid tests/operators (`F63`), and bad type hints (`F7`).
- **Interview Talking Point:** "We optimized CI speed and developer experience by prioritizing serious runtime-crashing bugs over strict styling rules, aligning with agile DataOps principles."

### Step 5: Security & Secret Detection
- **Purpose:** A lightweight, custom security check to prevent AWS credential leakage.
- **Mechanism:** Uses `grep` to scan for patterns resembling `AKIA` AWS access keys or hardcoded `aws_access_key_id` assignments. It specifically excludes the `.git` directory and uses quiet mode (`-q`) so that if a secret is found, the CI fails securely *without* echoing the secret to the GitHub Actions logs.
- **Interview Talking Point:** "Security is shifted left. Before any code is deployed or run in Airflow, we ensure no hardcoded AWS secrets are committed. We also protect the CI logs themselves by failing silently when a pattern is matched."

## 3. What a Green CI Run Proves (Interview Summary)

When this CI pipeline passes, it proves to the team (and to interviewers) that:
1. **Code is Syntactically Sound:** No obvious runtime crashes due to bad Python syntax or undefined variables.
2. **Architecture is Intact:** The required scripts for Kafka and Airflow are exactly where they need to be.
3. **Security is Enforced:** No glaring AWS credentials have been leaked into the codebase.
4. **Ready for Airflow:** The codebase is healthy enough to be picked up by the Airflow orchestrator for actual AWS deployment.

## 4. Troubleshooting CI Failures
- **Syntax/Linting Failure:** Review the exact line number flagged in the GitHub Actions logs and fix the syntax or undefined variable locally.
- **Structure Validation Failure:** Revert any accidental renaming or moving of core files (`producer.py`, `consumer.py`, `ecommerce_pipeline.py`).
- **Secret Detection Failure:** **Do not check the CI logs (they are hidden by design).** Immediately search locally for leaked AWS keys, remove them, rotate them in AWS IAM, and utilize `.env` files or AWS Profiles instead.
