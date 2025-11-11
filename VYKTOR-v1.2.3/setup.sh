#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 dashboard/server.py &
sleep 1
python3 vyktor.py
