import boto3
from pprint import pprint

client = boto3.client('ec2', region_name='us-east-1')
results = (
    client.get_paginator('describe_instances').paginate(
        PaginationConfig={
            'MaxItems': 5,
            'PageSize': 5
        }
    ).build_full_result()
)

pprint(results)
print(len(results['Reservations']))
pprint(results['Reservations'][0])
