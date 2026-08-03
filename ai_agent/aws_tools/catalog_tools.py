import boto3
import botocore.exceptions
from typing import Dict, Any
from ai_agent.config import GLUE_REGION

def get_table_schema(database_name: str, table_name: str) -> Dict[str, Any]:
    """
    Retrieves the table schema from AWS Glue Data Catalog.
    """
    try:
        session = boto3.Session(region_name=GLUE_REGION)
        client = session.client("glue")
        
        response = client.get_table(
            DatabaseName=database_name,
            Name=table_name
        )
        
        table = response.get("Table", {})
        
        columns = [
            {"name": col.get("Name"), "type": col.get("Type")}
            for col in table.get("StorageDescriptor", {}).get("Columns", [])
        ]
        
        partition_keys = [
            {"name": col.get("Name"), "type": col.get("Type")}
            for col in table.get("PartitionKeys", [])
        ]
        
        return {
            "database": database_name,
            "table": table_name,
            "columns": columns,
            "partition_keys": partition_keys,
            "location": table.get("StorageDescriptor", {}).get("Location", "UNKNOWN")
        }
        
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        error_msg = e.response['Error']['Message']
        if error_code == "EntityNotFoundException":
            return {"error": f"Table '{table_name}' in database '{database_name}' not found."}
        elif error_code == "AccessDeniedException":
            return {"error": f"Access Denied to Data Catalog: {error_msg}"}
        else:
            return {"error": f"AWS API Error: {error_msg}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
