# parsing s3 event notification from sns topic

import json
from pprint import pprint

with open("/home/kpit/Downloads/s3 event notification from sns topic.json") as json_file:
    json_data = json.load(json_file)

for record in json_data['Records']:
    messages = record['Sns']['Message']
    if isinstance(messages, str):
        messages = json.loads(messages)

    for message in messages.get('Records', []):
        pprint(message)
