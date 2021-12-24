#!/bin/bash

cd /app
python3.8 -m pip install --user virtualenv
virtualenv venv --python=python3.8
source venv/bin/activate
pip install -r requirements.txt
mkdir -p /app/out
mkdir -p /app/log
chown -R ec2-user:ec2-user /app
cp app.service /lib/systemd/system
systemctl daemon-reload