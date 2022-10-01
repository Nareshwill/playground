from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://demouser1:password@localhost/?authSource=close_loop_validation')
database = client['close_loop_validation']


@app.route('/insert_data', methods=['POST'])
def insert_data():
    payload = request.get_json()
    collection = database['unstructured_collection']
    ack = collection.insert_one(payload)
    print(ack)
    return {'message': 'success'}


if __name__ == '__main__':
    app.run()
