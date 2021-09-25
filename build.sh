#!/bin/bash

rm -rf package/*
cp *.py package/
cp -r awsgi package/
cp -r src/*.json package/
pip install -r requirements.txt -t ./package/

mkdir -p dist
cd ./package/
zip -r ../dist/lambda.zip .
