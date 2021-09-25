#!/bin/bash

rm -rf package/*
cp *.py package/
cp -r awsgi package/
cp -r src/*.json package/
pip3 install -r requirements.txt -t ./package/

mkdir -p dist
cd ./package/
zip -r ../dist/lambda.zip .
