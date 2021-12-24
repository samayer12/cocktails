#!/bin/bash
cd /app
source venv/bin/activate
python3.8 main.py recipes/ log.txt & exit 0