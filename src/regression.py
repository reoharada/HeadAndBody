import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import json
import math


class HeadBodyRegression:
    def __init__(self, deg=1):
        self.model_lr = None
        self.sscaler = preprocessing.StandardScaler()
        self.poly = PolynomialFeatures(deg) # 非線形次数
        self.labels = []
        self.x = []
        self.y = []
        self.xss = []
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
        x_poly = self.poly.fit_transform(self.x)
        self.sscaler.fit(x_poly)
        self.xss = self.sscaler.transform(x_poly)
        self.sscaler.fit(self.y)
        self.yss = self.sscaler.transform(self.y)

    def _modeling(self):
        _x = []
        _y = []
        with open('1632543141.json', 'r') as f:
            data = json.load(f)
            for d in data:
                _x.append([
                    self._distance_points(d, 'head_top_point', 'jaw_point'),
                    self._distance_points(d, 'right_shoulder_point', 'left_shoulder_point'),
                    self._distance_points(d, 'right_year_point', 'left_year_point'),
                    self._distance_points(d, 'left_year_point', 'jaw_point'),
                    self._distance_points(d, 'right_year_point', 'jaw_point'),
                ])
                _y.append(d['body_rate_by_head'])
        self.labels = [
            'head_jaw_distance',
            'shoulder_distance',
            'ear_distance',
            'l_ear_jaw_distance',
            'r_ear_jaw_distance',
        ]
        self.x = pd.DataFrame(_x, columns=self.labels)
        self.y = pd.DataFrame(_y, columns=['body_rate_by_head'])
        #print(self.x)
        #print(self.y)
        self._preprocess()
        self.model_lr = LinearRegression()
        self.model_lr.fit(self.xss, self.yss)

    def predict(self, x):
        x_df = pd.DataFrame(x, columns=self.labels)
        x_poly = self.poly.fit_transform(x_df)
        _sscaler = preprocessing.StandardScaler()
        _sscaler.fit(x_poly)
        xss_df = _sscaler.transform(x_poly)
        return self.sscaler.inverse_transform(self.model_lr.predict(xss_df))
        #return self.sscaler.inverse_transform(self.model_lr.predict(self.xss))

def main():
    reg = HeadBodyRegression(7) # モデル作成(遅い)
    input_x = []
    input_x.append([
        141.35258810969984,
        261.8101417441571,
        128.14054783713078,
        78.73019669346806,
        88.67042309827627
    ])
    print(reg.predict(input_x)[0][0])

if __name__ == "__main__":
    main()

