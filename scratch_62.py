import os.path

import boto3
import traceback
from botocore import exceptions
from pymongo import MongoClient

URI = 'mongodb://demouser1:password@localhost:27017/?authSource=close_loop_validation_pre_m2'
client = MongoClient(URI)
database = client['close_loop_validation_pre_m2']

topology_id = '1fffc901-b6d4-4c5e-a4b0-9cae8a06b41a'

print(database.list_collection_names())
scenario_status_record = database['scenario_status_record']

l0_collision_check = database['l0_collision_check']
kpi_cursor = l0_collision_check.find({'cad_topology_job_uuid': topology_id},
                                     {'_id': 0, 'scenario_uuid': 1, 'test_run_id': 1})
kpi_results = [f'{info.get("scenario_uuid")}#{info.get("test_run_id")}' for info in kpi_cursor]

print(len(kpi_results))

scenario_cursor = scenario_status_record.find({'cad_topology_job_uuid': topology_id},
                                              {'_id': 0, 'scenario_uuid': 1, 'test_run_id': 1})
scenario_results = [f'{info.get("scenario_uuid")}#{info.get("test_run_id")}' for info in scenario_cursor]
print(len(scenario_results))

diff = [info for info in scenario_results if info not in kpi_results]
print(len(diff))

total_diff = list()

s3_client = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'cclp-migration-data-test-02'

for data in diff:
    scenario_uuid, test_run_id = data.split('#')
    cursor = l0_collision_check.find({'scenario_uuid': scenario_uuid})
    if len(list(cursor)) and len(list(cursor)) != 1:
        print("Duplicates", data)
    key = os.path.join('data', 'bench1', test_run_id, 'Reprocessed_Output', f'xosc_{scenario_uuid}',
                       'ground_truth_kpi.parquet')
    try:
        response = s3_client.head_object(
            Bucket=BUCKET_NAME, Key=key)
        print(key, 'Size ', response.get("ContentLength", 0) / 1048576)
    except (Exception,
            exceptions.UnknownKeyError,
            exceptions.ClientError) as error:
        print(traceback.format_exc())
        print(error)

# print(len(total_diff))
