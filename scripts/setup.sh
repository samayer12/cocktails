#!/bin/bash

virtualenv venv --python=python3.8
source venv/bin/activate
pip3 install -r requirements.txt
mkdir -p /app/out
mkdir -p /app/log
echo "Setup Complete. Try running main.py"
