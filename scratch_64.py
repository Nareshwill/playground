import csv
import os.path
import boto3
import traceback
from botocore import exceptions
from pprint import pprint

from pymongo import MongoClient

client = MongoClient("mongodb://demouser1:password@localhost:27017/?authSource=close_loop_validation_pre_m2")
database = client['close_loop_validation_pre_m2']
scenario_status_record = database['scenario_status_record']

print(scenario_status_record.count_documents({'cad_topology_job_uuid': '1fffc901-b6d4-4c5e-a4b0-9cae8a06b41a'}))
cursor = scenario_status_record.find({'cad_topology_job_uuid': '1fffc901-b6d4-4c5e-a4b0-9cae8a06b41a'})
total_files = list()

s3_client = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'cclp-migration-data-test-02'
count = 1
file_info = list()

for doc in cursor:
    path = os.path.join('data', 'bench1', doc.get('test_run_id'), 'Reprocessed_Output',
                        f'xosc_{doc.get("scenario_uuid")}', 'ground_truth_kpi.parquet')
    try:
        response = s3_client.head_object(
            Bucket=BUCKET_NAME, Key=path)
        meta_info = {
            'slno': count,
            'path': path,
            'size': response.get("ContentLength", 0),
            'lastModified': response.get('LastModified').strftime("%d-%m-%Y, %H:%M:%S")
        }
        print(path, 'Size ', response.get("ContentLength", 0))
        file_info.append(meta_info)
    except (Exception,
            exceptions.UnknownKeyError,
            exceptions.ClientError) as error:
        print(traceback.format_exc())
        print(error)
    total_files.append(path)

    count += 1

print("Total files: ", len(total_files))
print("Total files without duplication", len(list(set(total_files))))

with open('ground_truth_files.csv', mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=[key for key in meta_info.keys()])
    writer.writeheader()
    writer.writerows(file_info)
