#!/bin/bash

cd /app
python3.8 -m pip3 install virtualenv
virtualenv venv --python=python3.8
source venv/bin/activate
pip3 install -r requirements.txt
mkdir -p /app/out
mkdir -p /app/log
chown -R ec2-user:ec2-user /app
echo "Setup Complete. Try running main.py"
