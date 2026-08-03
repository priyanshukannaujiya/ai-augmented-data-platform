import boto3
import time
import botocore.exceptions
from typing import Dict, Any
from ai_agent.config import GLUE_REGION, GOLD_DATABASE, ATHENA_OUTPUT_LOCATION

def run_athena_query(sql: str) -> Dict[str, Any]:
    """
    Executes a read-only Athena query on the Gold database and returns results.
    """
    # 1. Security Check: Only allow SELECT queries
    sql_upper = sql.upper().strip()
    if not sql_upper.startswith("SELECT"):
        return {"error": "Security exception: Only SELECT queries are permitted."}
    
    mutating_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", "TRUNCATE", "MERGE", "UNLOAD"]
    for kw in mutating_keywords:
        if kw in sql_upper:
            return {"error": f"Security exception: Query contains forbidden keyword '{kw}'."}
            
    # Add a LIMIT if none is present to prevent massive data pulls
    if "LIMIT" not in sql_upper:
        sql = f"{sql} LIMIT 50"
        
    try:
        session = boto3.Session(region_name=GLUE_REGION)
        client = session.client("athena")
        
        # 2. Submit the query
        response = client.start_query_execution(
            QueryString=sql,
            QueryExecutionContext={
                'Database': GOLD_DATABASE
            },
            ResultConfiguration={
                'OutputLocation': ATHENA_OUTPUT_LOCATION
            },
            WorkGroup='primary'
        )
        
        query_execution_id = response['QueryExecutionId']
        
        # 3. Poll for completion
        status = 'QUEUED'
        while status in ['QUEUED', 'RUNNING']:
            time.sleep(1)
            status_response = client.get_query_execution(QueryExecutionId=query_execution_id)
            status = status_response['QueryExecution']['Status']['State']
            
            if status in ['FAILED', 'CANCELLED']:
                reason = status_response['QueryExecution']['Status'].get('StateChangeReason', 'Unknown reason')
                return {"error": f"Query {status}: {reason}"}
                
        # 4. Retrieve results
        results_response = client.get_query_results(
            QueryExecutionId=query_execution_id,
            MaxResults=100
        )
        
        # 5. Convert results into structured Python/JSON data
        rows = results_response.get('ResultSet', {}).get('Rows', [])
        if not rows:
            return {"columns": [], "rows": []}
            
        # The first row contains the column names
        column_names = [col.get('VarCharValue', '') for col in rows[0].get('Data', [])]
        
        data_rows = []
        for row in rows[1:]:
            row_data = [col.get('VarCharValue', '') for col in row.get('Data', [])]
            # Map column names to values
            row_dict = dict(zip(column_names, row_data))
            data_rows.append(row_dict)
            
        return {
            "columns": column_names,
            "rows": data_rows,
            "query_id": query_execution_id
        }
        
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        error_msg = e.response['Error']['Message']
        return {"error": f"Athena API Error [{error_code}]: {error_msg}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
