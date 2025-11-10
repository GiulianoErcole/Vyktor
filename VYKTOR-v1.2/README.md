# VYKTOR v1.2 (DEV) — Distributed Evolution Update
### © 2025 NERON Intelligence Systems — Internal Experimental Research Prototype

**What’s new:**
- Parallelized evaluation (multi-core via `ProcessPoolExecutor`)
- Persistent gene pool (SQLite at `results/gene_pool.sqlite`)
- Optional Docker sandbox backend (`VYKTOR_BACKEND=docker`)
- Zero-dependency live dashboard (`dashboard/server.py`)

## Run
```bash
python3 vyktor.py
# Dashboard:
python3 dashboard/server.py  # http://127.0.0.1:8080
```

## Docker (optional)
```bash
cd sandbox
docker build -t vyktor-sandbox:latest .
cd ..
export VYKTOR_BACKEND=docker
python3 vyktor.py
```
