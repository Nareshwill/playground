import os
from datetime import datetime
import boto3
import uuid
from pymongo import MongoClient

client = MongoClient("mongodb://nareshc3:password@localhost:27017/?authSource=s3_triggers")
database = client['s3_triggers']
collection = database['upload_history']

_ = {'Records': [
    {'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2022-06-01T11:18:19.652Z',
     'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDA5IQJTL5TIHPE33TC7'},
     'requestParameters': {'sourceIPAddress': '103.28.246.246'},
     'responseElements': {'x-amz-request-id': '06NZ641ZKWD8PFSB',
                          'x-amz-id-2': 'zocEM+YTVB6xZvb6zHJM1A6eVOjocnW2DixbRZuqa7IRmWY0hEtId4vKqXkJOskaYT3BX/4iTly5TJgVOG8bndmj1FxiYtNg'},
     's3': {'s3SchemaVersion': '1.0', 'configurationId': '3a0c0e49-1bd2-4452-a612-96bedcd362fb',
            'bucket': {'name': 'my-athena-scenario', 'ownerIdentity': {'principalId': 'A3B8UDQNQSR6WA'},
                       'arn': 'arn:aws:s3:::my-athena-scenario'}, 'object': {
             'key': 'data/bench1/1654082294814-56012f0d-20ce-4413-87f1-9b2ccbfce067-i-0151e095ae5e9626a/Reprocessed_Output/xosc_0d90e365-2e24-4c2e-87a7-b65a370b3267/ground_truth_kpi.parquet',
             'size': 5842833, 'eTag': '957fa5f3ae62670302ba7448bdfdd4cd', 'sequencer': '0062974AF7E53E2144'}}}]}

if __name__ == "__main__":
    base_path = os.path.join("data", "bench1")
    test_run_id, _ = str(datetime.now().timestamp() * 1000).split('.')
    instance_id = "i-0151e095ae5e9626a"
    docker_id = str(uuid.uuid4())
    test_run_id = f"{test_run_id}-{docker_id}-{instance_id}"
    scenario_uuid = f"xosc_{str(uuid.uuid4())}"
    ground_truth_file = "ground_truth_kpi.parquet"
    path = os.path.join(base_path, test_run_id, 'Reprocessed_Output', scenario_uuid, ground_truth_file)
    bucket_name = "my-athena-scenario"

    client = boto3.client("s3")
    client.upload_file(ground_truth_file, bucket_name, path)
    collection.update_one({"path": path}, {
        "$set": {
            "path": path,
            "bucket_name": bucket_name,
            "created_at": datetime.now()
        }
    }, upsert=True)
    print(f"{datetime.now()} Uploaded!!!!")
