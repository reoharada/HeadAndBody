# HeadAndBody
## 環境
### pythonのバージョン
```
$ python --version
Python 3.9.6
```
### webフレームワーク
* Flask
### インフラ
* AWS APIGateway
* AWS Lambda
## 環境構築
### pipインストール
```
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py
$ which pip
/opt/homebrew/bin/pip
```
### パッケージインストール
```
$ pip install -t site-packages -r requirements.txt 
```
### ローカル環境起動
```
APP_ENV=development PYTHONPATH=`pwd`/site-packages python app.py 
```
http://127.0.0.1:8000/ or http://localhost:8000/ にアクセスできればOK
## 新規パッケージの追加
```
$ pip install -t site-packages パッケージ名
```
## AWS Lambdaビルド手順
```
$ ./build.sh
```
`dist/lambda.zip`をAWS Lambdaにアップロードする
## その他
`awsgi`はAWS APIGateway V2にまだ未対応らしい
https://github.com/slank/awsgi/issues/67
上記の修正を行い、独自に`awsgi/`以下に対応版を書き出している
awsgiがAPIGateway V2に対応次第、pipパッケージとして利用する

