#!/bin/sh
pipenv install
export FLASK_APP=./myix_api/index.py
source $(pipenv --venv)/bin/activate
FLASK_DEBUG=1 flask run -h 0.0.0.0
