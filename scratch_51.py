import json
import boto3

print('Loading function')


def lambda_handler(event, context):
    print('------------------------')
    print(event)
    # 1. Iterate over each record
    try:
        for record in event['Records']:
            # 2. Handle event by type
            if record['eventName'] == 'INSERT':
                handle_insert(record)
        print('------------------------')
        return "Success!"
    except Exception as e:
        print(e)
        print('------------------------')
        return "Error"


def handle_insert(record):
    print("Handling INSERT Event")

    # Get newData content
    new_iot_event = record['dynamodb']['newIOTevent']

    # Parse values
    new_device_id = new_iot_event['Device_ID']['S']
    new_timestamp = new_iot_event['timeStamp']['S']

    # Print it
    print('New row added with Device_ID=' + new_device_id)
    print("Done handling INSERT Event")