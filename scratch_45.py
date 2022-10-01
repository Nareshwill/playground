import time
from pprint import pprint

import boto3


def get_athena_results_paginator(params, athena_client):
    """
    :param params:
    :param athena_client:
    :return:
    """
    query_id = athena_client.start_query_execution(
        QueryString=params['query'],
        QueryExecutionContext={
            'Database': params['database']
        },
        ResultConfiguration={
            'OutputLocation': f"s3://{params['bucket']}/{params['path']}"
        },
        # WorkGroup=params['workgroup']
    )['QueryExecutionId']
    query_status = None
    while query_status == 'QUEUED' or query_status == "RUNNING" or query_status is None:
        query_status = athena_client.get_query_execution(QueryExecutionId=query_id)['QueryExecution']['Status']['State']
        if query_status == 'FAILED' or query_status == 'CANCELLED':
            raise Exception(f"Athena query with the string {params.get('query')} failed or cancelled")
        time.sleep(10)

    results_paginator = athena_client.get_paginator('get_query_results')
    results_iter = results_paginator.paginate(
        QueryExecutionId=query_id,
        PaginationConfig={
            'PageSize': 1000
        }
    )
    count, results = result_to_list_of_dict(results_iter)
    return results, count


def result_to_list_of_dict(results_iter):
    """
    :param results_iter:
    :return:
    """
    results = list()
    column_names = None
    count = 0
    for results_page in results_iter:
        print(len(list(results_iter)))
        for row in results_page['ResultSet']['Rows']:
            count += 1
            column_values = [col.get("VarCharValue", None) for col in row['Data']]
            if not column_names:
                column_names = column_values
            else:
                results.append(dict(zip(column_names, column_values)))
    return count, results


l1_longitudinal_jerk_kpi_table = """
    CREATE EXTERNAL TABLE IF NOT EXISTS `kpi_evaluation`.`l1_longitudinal_jerk_kpi_table` (
    `timestamp` bigint,
    `current_timestamp` double,
    `ego_velocity_x` double,
    `ego_acc_x` double
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
    WITH SERDEPROPERTIES (
    'serialization.format' = '1'
    ) LOCATION 's3://my-athena-scenario/data/bench1/1620996313492/Reprocessed_Output/xosc_8e062586-1b26-4043-8b75-94c061b201bf'
    TBLPROPERTIES ('has_encrypted_data'='false');
"""

rss_longitudinal_safe_check_kpi_query = """
    WITH 
        Q1 AS (SELECT
        CASE 
            WHEN ad_start = '1' AND rss_long_current <> '' THEN overall_rss_flag
            WHEN ad_start = '1.0' AND rss_long_current <> '' THEN overall_rss_flag
            ELSE 'True'
        END AS overall_rss, timestamp
        FROM rss_longitudinal_safe_check_kpi_csv)
    SELECT COUNT(Q1.overall_rss) AS NumberOfFalseCount FROM Q1 WHERE Q1.overall_rss = 'False';
"""

rss_lateral_left_safe_check_kpi_table = """
    CREATE EXTERNAL TABLE IF NOT EXISTS `kpi_evaluation`.`rss_lateral_left_safe_check_kpi_table` (
    `timestamp` bigint,
    `ad_start` string,
    `rss_lat_left_current` string,
    `rss_lat_left_safe` string,
    `rss_lat_left_flag` string,
    `overall_rss_flag` string
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
    WITH SERDEPROPERTIES (
    'serialization.format' = '1'
    ) LOCATION 's3://my-athena-scenario/data/bench1/1620996313492/Reprocessed_Output/xosc_8e062586-1b26-4043-8b75-94c061b201bf'
    TBLPROPERTIES ('has_encrypted_data'='false');
"""

rss_lateral_left_safe_check_kpi_query = """
    WITH 
        Q1 AS (SELECT
        CASE 
            WHEN ad_start = '1' AND rss_lat_left_current <> '' THEN overall_rss_flag
            WHEN ad_start = '1.0' AND rss_lat_left_current <> '' THEN overall_rss_flag
            ELSE 'True'
        END AS overall_rss
        FROM rss_lateral_left_safe_check_kpi_table)
    SELECT COUNT(Q1.overall_rss) AS NumberOfFalseCount FROM Q1 WHERE Q1.overall_rss = 'False';
"""

rss_lateral_right_safe_check_kpi_table = """
    CREATE EXTERNAL TABLE IF NOT EXISTS `kpi_evaluation`.`rss_lateral_right_safe_check_kpi_table` (
    `timestamp` bigint,
    `ad_start` string,
    `rss_lat_right_current` string,
    `rss_lat_right_safe` string,
    `rss_lat_right_flag` string,
    `overall_rss_flag` string
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
    WITH SERDEPROPERTIES (
    'serialization.format' = '1'
    ) LOCATION 's3://my-athena-scenario/data/bench1/1620996313492/Reprocessed_Output/xosc_8e062586-1b26-4043-8b75-94c061b201bf'
    TBLPROPERTIES ('has_encrypted_data'='false');
"""


rss_lateral_right_safe_check_kpi_query = """
    WITH 
        Q1 AS (SELECT
        CASE 
            WHEN ad_start = '1' AND rss_lat_right_current <> '' THEN overall_rss_flag
            WHEN ad_start = '1.0' AND rss_lat_right_current <> '' THEN overall_rss_flag
            ELSE 'True'
        END AS overall_rss
        FROM rss_lateral_right_safe_check_kpi_table)
    SELECT COUNT(Q1.overall_rss) AS NumberOfFalseCount FROM Q1 WHERE Q1.overall_rss = 'False';
"""


ground_truth_kpi_table = """
    CREATE EXTERNAL TABLE IF NOT EXISTS `kpi_evaluation`.`ground_truth_kpi_table` (
    `timestamp` bigint,
    `ego_alive` string,
    `current_timestamp` string,
    `new_timestamp` string,
    `waypoint` string,
    `right_lane_waypoint` string,
    `left_lane_waypoint` string,
    `ego_location_x` string,
    `ego_location_y` string,
    `ego_location_z` string,
    `ego_acc_x` double,
    `ego_acc_y` string,
    `throttle` string,
    `ego_velocity_x` string,
    `ego_velocity_y` string,
    `ego_length_half` string,
    `target_location_x` string,
    `target_location_y` string,
    `target_location_z` string,
    `target_velocity_x` string,
    `target_velocity_y` string,
    `target_length_half` string,
    `steer` string,
    `brake` string,
    `frame` string,
    `Server_response` string,
    `Touch_steer` string,
    `ad_start` string,
    `alc_set` string,
    `L2B2` string,
    `AD_DrvReqVel` string,
    `Indicator_State` string,
    `ego_width_half` string,
    `ego_forward_vector` string,
    `ego_road_id` string,
    `ego_lane_id` string,
    `ego_s_dist` string,
    `right_lane_type` string,
    `left_lane_type` string,
    `right_lanemarking_type` string,
    `left_lanemarking_type` string,
    `speed_limit` string,
    `ego_yaw` string,
    `target_width_half` string,
    `target_vehicle_waypoint` string,
    `target_vehicle_road_id` string,
    `target_vehicle_lane_id` string,
    `target_vehicle_s_dist` string,
    `traffic_vehicle_location_x` string,
    `traffic_vehicle_location_y` string,
    `traffic_vehicle_location_z` string,
    `traffic_vehicle_velocity_x` string,
    `traffic_vehicle_velocity_y` string,
    `traffic_vehicle_length_half` string,
    `traffic_vehicle_width_half` string,
    `traffic_vehicle_waypoint` string,
    `traffic_vehicle_right_waypoint` string,
    `traffic_vehicle_left_waypoint` string,
    `traffic_vehicle_road_id` string,
    `traffic_vehicle_lane_id` string,
    `traffic_vehicle_s_dist` string,
    `traffic_vehicle_sp_lim` string,
    `rss_long_current` string,
    `rss_long_safe` string,
    `rss_long_flag` string,
    `rss_lat_right_current` string,
    `rss_lat_right_safe` string,
    `rss_lat_right_flag` string,
    `rss_lat_left_current` string,
    `rss_lat_left_safe` string,
    `rss_lat_left_flag` string,
    `overall_rss_flag` string
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
    WITH SERDEPROPERTIES (
    'serialization.format' = '1'
    ) LOCATION 's3://my-athena-scenario/data/bench1/1620996313492/Reprocessed_Output/xosc_8e062586-1b26-4043-8b75-94c061b201bf'
    TBLPROPERTIES ('has_encrypted_data'='false');
"""

l1_longitudinal_jerk_kpi_view = """
    CREATE OR REPLACE VIEW l1_longitudinal_jerk_view AS
    SELECT timestamp, ego_acc_x
    FROM ground_truth_kpi_table;
"""

l1_longitudinal_jerk_kpi_query = """
    SELECT SUM(ego_acc_x) AS acceleration_x
    FROM (
        SELECT timestamp, ego_acc_x, 
        FIRST_VALUE(timestamp) OVER (ORDER BY timestamp) AS initial_timestamp
        FROM ground_truth_kpi_table
    ) WHERE timestamp BETWEEN timestamp AND initial_timestamp;
"""


if __name__ == "__main__":
    start_time = time.time()
    client = boto3.client("athena")
    parameters = {
        "database": "kpi_evaluation",
        "bucket": "my-athena-scenario",
        "path": "",
        "query": l1_longitudinal_jerk_kpi_query
    }
    query_results, counter = get_athena_results_paginator(
        params=parameters,
        athena_client=client
    )
    # print('count', counter)
    pprint(query_results)
    # for result in query_results:
    #     if int(result.get("NumberOfFalseCount", 0)) == 0:
    #         print('pass')
    #     else:
    #         print('fail')
    print(time.time() - start_time, "seconds")
