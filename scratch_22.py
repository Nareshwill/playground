from io import BytesIO

import yaml
from flask import Flask, send_file, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)


@app.route('/create_yaml')
def create_yaml_file():
    data = {
        'a': ['contains', 'something'],
    }
    memory_file = BytesIO()
    memory_file.write(bytes(yaml.dump(data=data, default_flow_style=False), 'utf-8'))
    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, attachment_filename='file.yaml')


@app.route('/index')
def index():
    return render_template('scratch_23.html')


if __name__ == '__main__':
    app.run()

# # Here we are import the Flask
# # class from flask package.
# from flask import Flask
#
# # Here we are instantiating with
# # Flask class with "__name__"
# # with this special variable inorder to
# # tell flask start point of our application
# app = Flask(__name__)
#
#
# # This route decorator mapped
# # with the index will get called
# # when an end user tries to access this
# # /index end point.
# @app.route('/index')  # Notice i haven't used the methods if u dont specify any methods by default GET method
# def index():
#     return {'data': 'Vikrant'}  # Returning an JSON response with 200 status code.
#
#
# if __name__ == '__main__':
#     app.run()  # Running the WSGI Server
