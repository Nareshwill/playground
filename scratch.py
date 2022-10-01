from flask import Flask, request

app = Flask(__name__)


@app.route("/get_data", methods=['POST'])
def get_data():
    payload = request.get_json()
    print(payload)
    print(type(payload))
    return {'message': 'success', 'data': payload}


@app.route("/fetch_info")
def fetch_info():
    return {'message': 'success', 'data': []}


@app.route("/fetch_data/")  # canonical URL
def fetch_data():
    return {'message': 'success', 'data': []}


if __name__ == '__main__':
    app.run()
