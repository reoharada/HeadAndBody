#!/bin/bash

rm -rf package/*
cp *.py package/
pip install -r requirements.txt -t ./package/

cd ./package/
zip -r ../dist/lambda.zip .
