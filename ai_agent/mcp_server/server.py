"""
MCP Server for the AWS Data Engineering Agent.
Exposes read-only tools to check AWS Glue job statuses.
"""

"""
MCP Server for the AWS Data Engineering Agent.
Exposes read-only tools to check AWS Glue job statuses.
"""

from mcp.server import MCPServer
import json
from ai_agent.aws_tools.glue_tools import get_glue_job_status
from ai_agent.aws_tools.catalog_tools import get_table_schema as catalog_schema_func
from ai_agent.aws_tools.athena_tools import run_athena_query as athena_query_func
from ai_agent.config import GLUE_JOB_BRONZE_TO_SILVER, GLUE_JOB_SILVER_TO_GOLD

mcp = MCPServer("AWS Data Engineering MCP Server")

@mcp.tool()
def glue_job_status(job_name: str) -> str:
    """
    Retrieves the latest Glue JobRun status for a given job name.
    """
    result = get_glue_job_status(job_name)
    return str(result)

@mcp.tool()
def get_table_schema(database_name: str, table_name: str) -> str:
    """
    Retrieves the table schema from AWS Glue Data Catalog.
    """
    result = catalog_schema_func(database_name, table_name)
    return json.dumps(result, indent=2)

@mcp.tool()
def run_athena_query(sql: str) -> str:
    """
    Executes a read-only Athena SQL query on the Gold database and returns the results.
    Only use SELECT queries.
    """
    result = athena_query_func(sql)
    return json.dumps(result, indent=2)

@mcp.tool()
def bronze_to_silver_status() -> str:
    """
    Retrieves the latest status of the Bronze-to-Silver ETL Glue Job.
    """
    result = get_glue_job_status(GLUE_JOB_BRONZE_TO_SILVER)
    return str(result)

@mcp.tool()
def silver_to_gold_status() -> str:
    """
    Retrieves the latest status of the Silver-to-Gold ETL Glue Job.
    """
    result = get_glue_job_status(GLUE_JOB_SILVER_TO_GOLD)
    return str(result)

if __name__ == "__main__":
    mcp.run()

