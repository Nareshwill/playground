import pymongo
from pprint import pprint

URI = "mongodb://demouser1:password@localhost:27017/?authSource=close_loop_validation"
client = pymongo.MongoClient(URI)
database = client['close_loop_validation']
# pprint(list(database.list_collections()))
collection = database.get_collection("topology")
record = collection.find_one({
    "$and": [
        {
            "$or": [
                {"docker1.scenario_group_id": 81},
                {"docker2.scenario_group_id": 81},
                {"docker3.scenario_group_id": 81},
                {"docker4.scenario_group_id": 81}
            ]
        }, {
            "$or": [
                {"docker1.test_point_id": 1459},
                {"docker2.test_point_id": 1459},
                {"docker3.test_point_id": 1459},
                {"docker4.test_point_id": 1459}
            ]
        }
    ],
    "job_id": "b291b587-10bf-451f-bc11-02a5bd0d61de",
    "cad_topology_job_uuid": "1c73125b-bd1a-4d2b-bad0-6f50a6b8fcce"
})
pprint(record)
