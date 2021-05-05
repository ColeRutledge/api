#!/usr/bin/env bash
pip list
pip3 install pip==20.1.1
pip list
pip3 install -r /app/requirements.txt
python3 entry.py db upgrade
python3 db_seed.py
python3 entry.py run -h 0.0.0.0:$PORT
# gunicorn app:app
