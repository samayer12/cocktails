#!/bin/bash
MIN_PYTHON_VER=3.8

source scripts/vercomp.sh

cd app/ 2>/dev/null || true

version=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')
if [[ -z "$version" ]]
then
    echo "No Python detected" 
    exit 1
fi

echo "Detected python version: $version."

vercomp "$version" $MIN_PYTHON_VER # Return codes: 0 is equal, 1 is greater, 2 is less

COMPARISON_CODE=$? 
if [ $COMPARISON_CODE -eq 2 ];
then
  echo "Current Python versions is less than required ($MIN_PYTHON_VER)."
  echo "Please upgrade your python version."
  exit 1
fi

echo "Creating virtual environment in: $(pwd)"
python3 -m pip install --user virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
echo "If running locally, try: sudo -E venv/bin/python3 src/main.py recipes log.txt"
