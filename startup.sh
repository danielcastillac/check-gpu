#!/bin/bash
set -x
/usr/bin/python3 -m pip install --upgrade pip
/usr/bin/python3 -m pip install --ignore-installed PyYAML
/usr/bin/python3 -m pip install -r /home/ubuntu/check-gpu/requirements.txt
gunicorn --bind 0.0.0.0:8001 -k uvicorn.workers.UvicornWorker app:app --daemon
