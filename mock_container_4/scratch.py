import os
import json
from pprint import pprint
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app=app)


class ScenarioStatus(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument(
            "bench_output_location",
            type=str,
            location="json",
            required=True,
            help="'bench_output_location' attribute is required"
        )

    def post(self):
        args = self.req_parse.parse_args()
        filename = "configuration.json"
        bench_config = dict()

        for root, _, files in os.walk(args['bench_output_location']):
            if filename in files:
                with open(os.path.join(root, filename)) as json_file:
                    bench_config = json.load(json_file)
        if bench_config and bench_config.get("video_list"):
            total_simulation = len(bench_config.get('video_list', []))
            executed_simulation = len([info for info in bench_config.get('video_list')
                                       if info['status'] == 'completed_with_success' or
                                       info['status'] == 'completed_with_error'])
            pprint(bench_config)
            print("total_simulation", total_simulation)
            print("executed_simulation", executed_simulation)
            return {'message': 'success', 'status': total_simulation == executed_simulation}
        return {'message': 'success', 'status': False}


api.add_resource(ScenarioStatus, "/container/get_execution_status")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9004)
