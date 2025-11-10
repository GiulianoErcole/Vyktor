# VYKTOR v1.2.1 - Stability & Insight (WebSocket Edition)
(c) 2025 NERON Intelligence Systems - Internal Experimental Research Prototype

## Install
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python3 vyktor.py
python3 dashboard/server.py  # open http://127.0.0.1:8080
```

## Optional Docker
```bash
cd sandbox && docker build -t vyktor-sandbox:latest . && cd ..
export VYKTOR_BACKEND=docker
python3 vyktor.py
```
