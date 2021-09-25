import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
import json
import math


class HeadBodyRegression:
    def __init__(self):
        self.model_lr = None
        self.sscaler = preprocessing.StandardScaler()
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

    def _standard(self):
        self.sscaler.fit(self.x)
        self.xss = self.sscaler.transform(self.x)
        self.sscaler.fit(self.y)
        self.yss = self.sscaler.transform(self.y)

    def _modeling(self):
        _x = []
        _y = []
        with open('1632543141.json', 'r') as f:
            data = json.load(f)
            for d in data:
                _x.append([
                    self._distance(d['right_year_point']['x'] - d['left_year_point']['x'],
                                   d['right_year_point']['y'] - d['left_year_point']['y']),
                    self._distance(d['right_shoulder_point']['x'] - d['left_shoulder_point']['x'],
                                   d['right_shoulder_point']['y'] - d['left_shoulder_point']['y'])
                ])
                _y.append(d['body_rate_by_head'])
        self.x = pd.DataFrame(_x, columns=['ear', 'shoulder'])
        self.y = pd.DataFrame(_y, columns=['body_rate'])
        print(self.x)
        print(self.y)
        self._standard()
        self.model_lr = LinearRegression()
        self.model_lr.fit(self.xss, self.yss)

    def predict(self, x):
        x_df = pd.DataFrame(x, columns=['ear', 'shoulder'])
        _sscaler = preprocessing.StandardScaler()
        _sscaler.fit(x_df)
        xss_df = _sscaler.transform(x_df)
        return self.sscaler.inverse_transform(self.model_lr.predict(xss_df))

def main():
    reg = HeadBodyRegression()
    input_x = []
    input_x.append([35, 60])
    print(reg.predict(input_x))

if __name__ == "__main__":
    main()
