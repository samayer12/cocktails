#!/bin/bash
cd /app
source venv/bin/activate
nohup python3.8 main.py recipes/ log.txt & exit 0