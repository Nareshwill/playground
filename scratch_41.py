import json
from queue import Queue
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://demouser1:password@localhost:27017/close_loop_validation"
api = Api(app=app)
mongo = PyMongo(app=app)

docker_log = mongo.db.docker_log


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


class QueueStream(object):
    def __init__(self, max_size=30):
        self.queue = Queue(maxsize=max_size)

    def enqueue(self, message):
        self.queue.put(message)

    def dequeue(self):
        return self.queue.get()

    def __len__(self):
        return self.queue.qsize()


docker_queue = QueueStream(max_size=50)


class DockerLog(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument(
            'container_id',
            location='json',
            required=True,
            help='"container_id" is not provided'
        )
        self.req_parse.add_argument(
            "block_io",
            location='json',
            required=True,
            help='"block_io" is not provided'
        )
        self.req_parse.add_argument(
            "cpu_perc",
            location='json',
            required=True,
            help='"cpu_perc" is not provided'
        )
        self.req_parse.add_argument(
            "mem_perc",
            location='json',
            required=True,
            help='"mem_perc" is not provided'
        )
        self.req_parse.add_argument(
            "mem_usage",
            location='json',
            required=True,
            help='"mem_usage" is not provided'
        )
        self.req_parse.add_argument(
            "container_name",
            location='json',
            required=True,
            help='"container_name" is not provided'
        )
        self.req_parse.add_argument(
            "container_created_at",
            location='json',
            required=True,
            help='"container_created_at" is not provided'
        )
        self.req_parse.add_argument(
            "image",
            location='json',
            required=True,
            help='"image" is not provided'
        )
        self.req_parse.add_argument(
            "ports",
            location='json',
            required=True,
            help='"ports" is not provided'
        )
        self.req_parse.add_argument(
            "running_for",
            location='json',
            required=True,
            help='"running_for" is not provided'
        )
        self.req_parse.add_argument(
            "size",
            location='json',
            required=True,
            help='"size" is not provided'
        )
        self.req_parse.add_argument(
            "state",
            location='json',
            required=True,
            help='"state" is not provided'
        )
        self.req_parse.add_argument(
            "status",
            location='json',
            required=True,
            help='"status" is not provided'
        )
        self.req_parse.add_argument(
            "timestamp",
            location='json',
            required=True,
            help='"timestamp" is not provided'
        )

    def post(self):
        args = self.req_parse.parse_args()
        timestamp = float(args['timestamp'])
        args.update({'updated_at': datetime.fromtimestamp(timestamp)})
        _ = docker_log.insert_one(args.copy())
        docker_queue.enqueue(message=args.copy())
        return {'message': 'success', 'args': json.dumps(args, cls=DatetimeEncoder)}, 200


class DockerStatistics(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument(
            "container_name",
            type=str,
            location='json',
            help='"container_name" is not provided'
        )
        self.req_parse.add_argument(
            "minutes",
            type=int,
            default=5,
            location='json',
            help='"duration" attribute is not provided'
        )

    def post(self):
        args = self.req_parse.parse_args()
        args = dict(args)
        now = datetime.now()
        start_time = now - timedelta(minutes=args['minutes'])
        container_name = args['container_name']
        record = docker_log.aggregate([
            {
                "$match": {
                    {
                        "$and": [
                            {
                                "updated_at": {"$gte": start_time, "$lte": now}
                            },
                            {
                                "container_name": container_name
                            }
                        ]
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "cpu_perc": 1,
                    "mem_perc": 1,
                    "mem_usage": 1
                }
            }
        ])
        return {'message': 'success'}


api.add_resource(DockerLog, '/log/docker_info')
api.add_resource(DockerStatistics, '/stats/dockers')

if __name__ == '__main__':
    app.run()
