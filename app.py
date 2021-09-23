import awsgi
import config
from flask import Flask, jsonify

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return jsonify({'head_and_boody_result': 7.4, 'APP_ENV': config.APP_ENV}), 200

@app.route('/hello', methods=['GET'])
def hello_get():
    return {'msg': 'get method'}

@app.route('/hello', methods=['POST'])
def hello_post():
    return {'msg': 'post method'}
    
def lambda_handler(event, context):
    return awsgi.response(app, event, context)

if config.APP_ENV == 'development': app.run(port=8000, debug=True)
