import boto3
from pprint import pprint

# {'ResponseMetadata': {'HTTPHeaders': {'content-length': '747',
#                                       'content-type': 'text/xml',
#                                       'date': 'Mon, 29 Aug 2022 12:22:34 GMT',
#                                       'x-amzn-requestid': '3e6b94fc-c21a-5931-a10f-cf7a73d089fd'},
#                       'HTTPStatusCode': 200,
#                       'RequestId': '3e6b94fc-c21a-5931-a10f-cf7a73d089fd',
#                       'RetryAttempts': 0},
#  'Topics': [{'TopicArn': 'arn:aws:sns:us-east-1:911626952550:ec2-status-topic'},
#             {'TopicArn': 'arn:aws:sns:us-east-1:911626952550:kpi-evaluation-from-sqs-standard'},
#             {'TopicArn': 'arn:aws:sns:us-east-1:911626952550:kpi-evaluation-from-sqs.fifo'},
#             {'TopicArn': 'arn:aws:sns:us-east-1:911626952550:kpi-standard-topic'}]}

client = boto3.client('sns', region_name='us-east-1')
# response = client.list_topics()

# Publish a message
message = {
        'scheduler_uuid': '6af24199-f0ec-4d2c-9f99-54b76e705ca5',
        'test_run_id': '1659518751190-084bd4e69d6f792b6-101e9dc2-0086-4eea-88c6-c3855e756441|i-084bd4e69d6f792b6',
        'scenario_group_id': 15,
        'scenario_uuid': '28c587a9-bd2e-4e95-88b7-d4fd2f20659e',
        'scenario_status': 'completed_with_success',
        'cad_topology_job_uuid': '1fffc901-b6d4-4c5e-a4b0-9cae8a06b41a',
        'job_id': 'd880ef85-664d-4d36-b8d0-3270e4037248',
        'bench_id': 11,
        'bench_name': 'Carla_Bench_1',
        'instance_id': 'i-084bd4e69d6f792b6',
        'docker_id': '101e9dc2-0086-4eea-88c6-c3855e756441|i-084bd4e69d6f792b6',
        'bucket_name': 'cclp-migration-data-test-02',
        'region_name': 'us-east-1',
    }
response = client.publish(
    TopicArn='arn:aws:sns:us-east-1:911626952550:kpi-evaluation-from-sqs-standard',
    Message=str(message),
    Subject='KPI Evaluation'
)
pprint(response)
