from flask import Flask, request

app = Flask(__name__)


@app.route('/greet', methods=['POST'])
def greet():
    payload = request.get_json()
    if "name" not in payload:
        return {'message': '"name" attribute is required'}, 400

    return {'message': f"Hello {payload['name']}"}


if __name__ == "__main__":
    app.run()
