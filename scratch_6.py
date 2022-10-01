import json

import pymongo

username = 'demouser1'
password = 'password'
database = 'close_loop_validation'
mongo_uri = "mongodb://{}:{}@localhost/{}?authSource={}".format(
    username,
    password,
    database,
    database)

client = pymongo.MongoClient(mongo_uri)
database = client[database]
collection = database['scenario_status_record']

with open('result.json') as json_file:
    data = json.load(json_file)

output = list()
for info in data:
    cursor = collection.find_one({'scenario_uuid': info['scenario_uuid']},
                                 {'_id': 0, 'scenario_uuid': 1, 'test_run_id': 1})
    if cursor:
        output.append(cursor)
    else:
        print('No Match found: {}'.format(info['scenario_uuid']))

with open('output.json', mode='w') as file_obj:
    json.dump(output, file_obj, indent=2)
