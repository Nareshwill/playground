import boto3
from pprint import pprint

client = boto3.client('ec2')
response = client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['cloud_machine_test']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['stopped']
        }
    ],
    MaxResults=5
)
if response.get('Reservations') and len(response.get('Reservations')) > 0:
    pprint(response)
