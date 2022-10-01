import uuid
from flask import Flask, request
from pprint import pprint

app = Flask(__name__)


@app.after_request
def after_request(response):
    print(request)
    print(request.endpoint)
    print(dir(request))
    print(response.status_code)
    print(response.data)
    return response


@app.route('/upload_file', methods=['GET'])
def upload_file():
    message = 'Random uuid: {}'.format(
        str(uuid.uuid4()))
    return {'message': 'success', 'response': message}


if __name__ == '__main__':
    app.run()
