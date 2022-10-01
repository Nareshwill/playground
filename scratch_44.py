import time
import boto3
from pprint import pprint

basic_query = """
    SELECT timestamp / 1000, overall_rss_flag, rss_long_current, (timestamp / 1000) - FIRST_VALUE(timestamp / 1000) OVER (ORDER BY timestamp)
    FROM rss_longitudinal_safe_check_kpi
    ORDER BY timestamp;
"""

case_query = """
    SELECT
    CASE 
        WHEN ad_start = '1' THEN overall_rss_flag
        WHEN ad_start = '1.0' THEN overall_rss_flag
        ELSE 'True'
    END AS overall_rss_flag, timestamp
    FROM rss_longitudinal_safe_check_kpi_csv;
"""

client = boto3.client("athena")
response_query_execution_id = client.start_query_execution(
    QueryString="""
        SELECT rss_long_current
        FROM
        rss_longitudinal_safe_check_kpi_csv;
    """,
    QueryExecutionContext={
        "Database": "kpi_evaluation"
    },
    ResultConfiguration={
        "OutputLocation": "s3://my-athena-scenario/"
    }
)
query_execution_id = response_query_execution_id['QueryExecutionId']

iterations = 360

while iterations > 0:
    iterations = iterations - 1
    response_get_query_details = client.get_query_execution(
        QueryExecutionId=query_execution_id
    )
    status = response_get_query_details['QueryExecution']['Status']['State']
    if status == "RUNNING" or status == "QUEUED":
        print(status)
        time.sleep(2)
        iterations += 1
    elif status == "SUCCEEDED":
        response_query_result = client.get_query_results(
            QueryExecutionId=query_execution_id
        )
        pprint(response_query_result)
        result_data = response_query_result['ResultSet']
        pprint(result_data)
        print(len(result_data.get('Rows')))
        break
    else:
        print(status)
        break

