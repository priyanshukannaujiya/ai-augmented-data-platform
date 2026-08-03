"""
AWS Glue tools for the AI agent.
Provides read-only access to AWS Glue job statuses.
"""

import boto3
import botocore.exceptions
from typing import Dict, Any, Optional

from ai_agent.config import GLUE_REGION, GLUE_JOB_BRONZE_TO_SILVER, GLUE_JOB_SILVER_TO_GOLD

def get_glue_job_status(job_name: str) -> Dict[str, Any]:
    """
    Retrieves the latest Glue JobRun status and returns structured data.
    
    Returns a dictionary containing:
    - job_name
    - job_run_id
    - status
    - started_on
    - completed_on
    - execution_time
    - error_message
    """
    try:
        session = boto3.Session(region_name=GLUE_REGION)
        client = session.client("glue")
        
        response = client.get_job_runs(
            JobName=job_name,
            MaxResults=1
        )
        
        job_runs = response.get("JobRuns", [])
        
        if not job_runs:
            return {
                "job_name": job_name,
                "status": "NOT_FOUND",
                "error_message": "No previous job runs found for this job."
            }
            
        latest_run = job_runs[0]
        
        # Extract required fields
        return {
            "job_name": job_name,
            "job_run_id": latest_run.get("Id", "UNKNOWN"),
            "status": latest_run.get("JobRunState", "UNKNOWN"),
            "started_on": latest_run.get("StartedOn", None),
            "completed_on": latest_run.get("CompletedOn", None),
            "execution_time": latest_run.get("ExecutionTime", 0),
            "error_message": latest_run.get("ErrorMessage", "")
        }
        
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        error_msg = e.response['Error']['Message']
        
        if error_code == "AccessDeniedException":
            return {
                "job_name": job_name,
                "status": "ACCESS_DENIED",
                "error_message": f"IAM User lacks permission to get job runs. Detailed Error: {error_msg}"
            }
        elif error_code == "EntityNotFoundException":
            return {
                "job_name": job_name,
                "status": "DOES_NOT_EXIST",
                "error_message": f"Glue job '{job_name}' does not exist in region {GLUE_REGION}."
            }
        else:
            return {
                "job_name": job_name,
                "status": "API_ERROR",
                "error_message": f"AWS API Error [{error_code}]: {error_msg}"
            }
    except Exception as e:
         return {
            "job_name": job_name,
            "status": "ERROR",
            "error_message": f"Unexpected error: {str(e)}"
         }

if __name__ == "__main__":
    jobs_to_test = [GLUE_JOB_BRONZE_TO_SILVER, GLUE_JOB_SILVER_TO_GOLD]
    
    print("="*60)
    print("AWS GLUE JOB STATUS CHECK")
    print("="*60)
    
    for job in jobs_to_test:
        print(f"\nChecking latest run for: {job}")
        status_data = get_glue_job_status(job)
        
        for key, value in status_data.items():
            # Format datetime objects nicely if present
            if key in ('started_on', 'completed_on') and value is not None:
                print(f"{key:>15}: {value.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            else:
                print(f"{key:>15}: {value}")
                
    print("\n" + "="*60)
