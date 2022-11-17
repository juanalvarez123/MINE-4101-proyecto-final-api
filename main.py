from flask import Flask
from flask import jsonify

from config import config


def create_app(arg_environment):
    local_app = Flask(__name__)
    local_app.config.from_object(arg_environment)
    return local_app


environment = config['development']
app = create_app(environment)


@app.route('/ping', methods=['GET'])
def get_ping():
    return 'pong'


@app.route('/predict', methods=['POST'])
def post_predict():
    return jsonify('Una predicción ...')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
