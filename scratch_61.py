import json
from pprint import pprint
from pymongo import MongoClient
from json.encoder import JSONEncoder
from bson import json_util
from typing import Any


class ObjectIdSerializer(JSONEncoder):
    def default(self, o: Any) -> Any:
        return json_util.default(o)


database_name = 'close_loop_validation_pre_m2'
client = MongoClient(f'mongodb://demouser1:password@localhost:27017/?authSource={database_name}')
database = client[database_name]

pprint(database.list_collection_names())

l0_collision_check = database['l0_collision_check']
cad_topology_job_uuid = '1fffc901-b6d4-4c5e-a4b0-9cae8a06b41a'
cursor = l0_collision_check.aggregate([
    {
        '$match': {
            'cad_topology_job_uuid': cad_topology_job_uuid
        }
    },
    {
        '$group': {
            '_id': None,
            'scenarioIds': {
                '$addToSet': '$scenario_uuid'
            }
        }
    },
    {
        '$lookup': {
            'from': 'scenario_drive_session',
            'let': {
                'scenarioIds': '$scenarioIds'
            },
            'pipeline': [
                {
                    '$match': {
                        '$expr': {
                            '$in': ['$scenario_uuid', '$$scenarioIds']
                        }
                    }
                },
                {
                    '$project': {
                        'file_name': 1,
                        'scenario_uuid': 1
                    }
                },
                {
                    '$addFields': {
                        'scenario': {
                            '$substr': [
                                '$file_name',
                                0,
                                {
                                    '$indexOfBytes': [
                                        '$file_name',
                                        '_Var'
                                    ]
                                }
                            ]
                        }
                    }
                },
                {
                    '$addFields': {
                        'scenario': {
                            '$substr': [
                                '$scenario',
                                {
                                    '$indexOfBytes': [
                                        '$scenario',
                                        'SC'
                                    ]
                                },
                                {
                                    '$strLenCP': '$scenario'
                                }
                            ]
                        }
                    }
                }
            ],
            'as': 'scenario_drive_session_details'
        }
    }
])
result = list(cursor)

pprint(result)
# print(result[0].keys())
# with open(f'{cad_topology_job_uuid}.json', mode='w') as json_file:
#     json.dump(result, json_file, indent=4, cls=ObjectIdSerializer)
print('Total ScenarioIds', len(result[0]['scenarioIds']))
print('Total Details', len(result[0]['scenario_drive_session_details']))

scenario_details = [info.get('scenario_uuid') for info in result[0]['scenario_drive_session_details']]
print('Total Scenario Details', len(scenario_details))
print('Without Duplicates', len(list(set(scenario_details))))

scenario_info_cursor = l0_collision_check.find({'cad_topology_job_uuid': cad_topology_job_uuid})
scenarios = [info.get('scenario_uuid') for info in scenario_info_cursor]
print('Total Scenarios ', len(scenarios))
print('Duplicates', len(list(set([scenario for scenario in scenario_details if scenarios.count(scenario) != 1]))))
