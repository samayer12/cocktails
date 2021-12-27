#!/bin/bash

python3.8 -m pip install --user virtualenv
virtualenv venv --python=python3.8
source venv/bin/activate
pip install -r requirements.txt
echo "If running locally, try sudo -E venv/bin/python3.8 main.py recipes log.txt"