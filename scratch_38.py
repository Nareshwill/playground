import logging
import traceback

import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app=app)


class DockerExecutionStatus(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument(
            "ports",
            location='json',
            type=list,
            required=True,
            help="'ports' attribute is required")
        self.req_parse.add_argument(
            "address",
            location='json',
            type=str,
            required=True,
            help="'address' attribute is required")
        self.req_parse.add_argument(
            "bench_output_location",
            location='json',
            type=str,
            required=True,
            help="'bench_output_location' attribute is required")

    def post(self):
        args = self.req_parse.parse_args()
        container_payload = {
            "bench_output_location": args['bench_output_location']
        }
        status = list()
        # payloads = [
        #     "/home/kpit/.config/JetBrains/PyCharmCE2021.3/scratches/mock_container_1/bench1",
        #     "/home/kpit/.config/JetBrains/PyCharmCE2021.3/scratches/mock_container_2/bench1",
        #     "/home/kpit/.config/JetBrains/PyCharmCE2021.3/scratches/mock_container_3/bench1",
        #     "/home/kpit/.config/JetBrains/PyCharmCE2021.3/scratches/mock_container_4/bench1"
        # ]
        for index, port in enumerate(args['ports']):
            # container_payload = {
            #     "bench_output_location": payloads[index]
            # }
            try:
                url = "http://{}:{}/container/get_execution_status".format(args['address'], port)
                logging.info("Making a request to the url: %s" % url)
                response = requests.post(url, json=container_payload)
                logging.info("Status code: %s", response.status_code)
                logging.info("Response (json): %s", response.json())
                if response.status_code == 200:
                    data = response.json()
                    status.append(data['status'])
                else:
                    status.append(False)
            except Exception as error:
                logging.error(str(error))
                logging.error(traceback)
                status.append(False)
        return {'message': 'success', 'status': status}


api.add_resource(DockerExecutionStatus, "/container/execution_status")

if __name__ == "__main__":
    logging.basicConfig(
        filename="status.log",
        format='%(asctime)s - %(message)s', level=logging.INFO)
    app.run(host='0.0.0.0')
