## v1.3.2-DEV PATCH2 — Consolidated Fix
- Includes PATCH1 fitness import fix in `core/scheduler.py`
- Ensures dashboard/server reads ports from env and prints version banner
- Adds `VERSION.txt` and README note for HERMES build

## v1.3.2-DEV — Project HERMES (Adaptive Fitness + PyTorch)
- Added multi-objective fitness combiner (`core/fitness.py`) and seed adapter
- Scheduler logs per-seed fitness; dashboard gets richer metrics
- New seeds: `autoencoder_seed.py` (PyTorch), `rle_codec.py`, `opt_entropy_seed.py`
- Dev ports: HTTP 8082 / WS 8767 (setup with `bash setup.sh --dev`)
- Requirements: PyTorch, NumPy, Matplotlib, sqlite-utils

