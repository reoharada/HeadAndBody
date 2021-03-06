import awsgi
import config
from flask import Flask, jsonify, request
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import json
import math

app = Flask(__name__, static_folder='.', static_url_path='')

class HeadBodyRegression:
    def __init__(self, deg=1):
        self.model_lr = None
        self.scaler_x = preprocessing.MinMaxScaler()
        self.scaler_y = preprocessing.MinMaxScaler()
        self.poly = PolynomialFeatures(deg) # 非線形次数
        self.labels = []
        self.x = []
        self.y = []
        self.xss = []
        self.xsp = []
        self.yss = []
        self._modeling()

    def _distance(self, x, y):
        xd = x ** 2
        yd = y ** 2
        dd = math.sqrt(xd + yd)
        return dd

    def _distance_points(self, data, u, v):
        return self._distance(data[u]['x'] - data[v]['x'], data[u]['y'] - data[v]['y'])

    def _preprocess(self):
        self.xss = self.scaler_x.fit_transform(self.x)
        self.xsp = self.poly.fit_transform(self.xss)
        self.yss = self.scaler_y.fit_transform(self.y)

    def _modeling(self):
        _x = []
        _y = []
        with open('src/1632543141.json', 'r') as f:
            data = json.load(f)
            for d in data:
                ear_distance = self._distance_points(d, 'right_year_point', 'left_year_point')
                _x.append([
                    self._distance_points(d, 'head_top_point', 'jaw_point') / ear_distance,
                    self._distance_points(d, 'right_shoulder_point', 'left_shoulder_point') / ear_distance,
                    #self._distance_points(d, 'left_year_point', 'jaw_point') / ear_distance,
                    #self._distance_points(d, 'right_year_point', 'jaw_point') / ear_distance,
                ])
                _y.append(d['body_rate_by_head'])
        self.labels = [
            'head_jaw_distance',
            'shoulder_distance',
            #'l_ear_jaw_distance',
            #'r_ear_jaw_distance',
        ]
        self.x = pd.DataFrame(_x, columns=self.labels)
        self.y = pd.DataFrame(_y, columns=['body_rate_by_head'])
        #print(self.x)
        #print(self.y)
        self._preprocess()
        #print(self.xsp)
        #print(self.yss)
        self.model_lr = LinearRegression()
        self.model_lr.fit(self.xsp, self.yss)

    def predict(self, x):
        x_df = pd.DataFrame(x, columns=self.labels)
        print(x_df)
        xss_df = self.scaler_x.transform(x_df)
        xsp_df = self.poly.fit_transform(xss_df)
        #print(xsp_df)
        return self.scaler_y.inverse_transform(self.model_lr.predict(xsp_df))
        #return self.scaler_y.inverse_transform(self.model_lr.predict(self.xsp))

@app.route('/')
def index():
    return jsonify({'head_and_boody_result': 7.4, 'APP_ENV': config.APP_ENV}), 200

@app.route('/', methods=['POST'])
def index_post():
    data = json.loads(request.data)
    print(data)
    distanceFromHeadToJaw = data['distance_from_head_to_jaw']
    distanceShoulders = data['distance_shoulders']
    distanceEars = data['distance_ears']
    #distanceFromLeftEraToJaw = data['distance_from_left_era_to_jaw']
    #distanceFromRightEraToJaw = data['distance_from_right_era_to_jaw']
    reg = HeadBodyRegression(3) # モデル作成(遅い)
    input_x = []
    input_x.append([distanceFromHeadToJaw / distanceEars, distanceShoulders / distanceEars])
    return jsonify({'head_and_boody_result': reg.predict(input_x)[0][0], 'APP_ENV': config.APP_ENV}), 200

@app.route('/hello', methods=['GET'])
def hello_get():
    return {'msg': 'get method'}

@app.route('/hello', methods=['POST'])
def hello_post():
    return {'msg': 'post method'}
    
def lambda_handler(event, context):
    return awsgi.response(app, event, context)

if config.APP_ENV == 'development': app.run(host='0.0.0.0', port=80, debug=True)
