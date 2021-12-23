#!/bin/bash

pwd
ls -l
pip3 install -r requirements.txt
mkdir -p /app/out
mkdir -p /app/log
echo "Setup Complete. Try running main.py"
