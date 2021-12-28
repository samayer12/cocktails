#!/bin/bash

cd app/ 2>/dev/null || true
echo "Creating virtual environment in: $(pwd)"
python3 -m pip install --user virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
echo "If running locally, try sudo -E venv/bin/python3 src/main.py recipes log.txt"