# 🧬 VYKTOR — CHANGELOG
### © 2025 NERON Intelligence Systems  


### Next Planned

---

## v1.3.3-DEV — Dashboard Upgrade (Live charts + Leaderboard)
- New `/dashboard.html` with live charts for Fitness, Runtime, Acceptance (no external JS deps)
- WebSocket-driven Top-10 seed leaderboard by best fitness score
- Telemetry snapshot panel refreshes every 3s (`/api/summary`)
- Version banner bumped to v1.3.3 DEV (DASH); honors `--dev` ports


---


## v1.3.2-DEV PATCH2 — Consolidated Fix
- Includes PATCH1 fitness import fix in core/scheduler.py
- Ensures dashboard/server reads ports from env and prints version banner
- Adds VERSION.txt


---


## v1.3.2-DEV — Project HERMES (Adaptive Fitness + PyTorch)
- Added multi-objective fitness combiner (`core/fitness.py`) and seed adapter
- Scheduler logs per-seed fitness; dashboard gets richer metrics
- New seeds: `autoencoder_seed.py` (PyTorch), `rle_codec.py`, `opt_entropy_seed.py`
- Dev ports: HTTP 8082 / WS 8767 (setup with `bash setup.sh --dev`)
- Requirements: PyTorch, NumPy, Matplotlib, sqlite-utils


---


## v1.3.1 — Seed Expansion (FULL)
- Integrated research-grade seeds: Huffman, LZ77, DPCM, Rabin–Karp, Bloom Filter, Karger Min-Cut,
  K-Means, TSP (SA), Symbolic Regression.
- Engine: same as v1.3.0-DEV (Trident, PATCH3) with telemetry + stable dashboard.


---


## v1.3.0-DEV — Trident (PATCH1)
- Fixed server global/port state; added /api/ports and reconnection logic
- Forced immediate evaluation → visible gen0 tick
- Lower default timeouts and rounds for snappier feedback
- Added 'seeds_loaded' event so dashboard is never idle at start
  

---


## v1.2.3 — Neural Bloom (Stable)
- Adaptive mutation & timeouts via config
- Per-generation metrics (OK %, avg runtime)
- Canvas charts + reconnecting WS dashboard
- Telemetry persistence (SQLite); history API


---

## v1.2.2 — Live & Loud
- Added continuous gen_tick events every generation
- Added session start header to live feed
- Added /api/summary endpoint and snapshot bootstrap for dashboard
- Dashboard replays last 50 log lines on connect
- New UI: pause/resume feed, lineage depth display, and status indicator
- Hardened log tailer (handles truncation and rotation)
- Fixed parallel evaluation write-back issue
- Minor code cleanup and stability improvements
  
---

## v1.2.1 - Stability & Insight
- Fixed parallel evaluation write-back bug
- WebSocket live dashboard (real-time)
- Updated docs and quickstart

---

## v1.2 — Distributed Evolution Update
**Date:** November 2025
- Parallelized mutation via multi-core scheduling  
- Persistent “gene pool” between runs  
- Docker-based sandboxing  
- Web dashboard for monitoring generations  

---

## v1.1.1 — Evolutionary Refinement Update
**Date:** November 2025  

- Improved multi-objective scoring (correctness, speed, brevity)  
- Added Top-K archival (stores top 5 candidates per task)  
- Expanded population size and generations (12 × 80)  
- Unified public + internal README documentation  
- Enhanced mutation tracking (`mut(mut(seed))` lineage)  
- General stability and logging improvements  

---

## v1.1 — NERON Integration Build
**Date:** November 2025  

- Rebranded under **NERON Intelligence Systems**  
- Removed all external dependencies (`ast.unparse()` replaces `astor`)  
- Added new seeds: `roman_to_int`, `levenshtein`, `lru_cache`  
- Improved mutation safety and scoring accuracy  
- Organized folder structure (`core/`, `data/`, `results/`)  
- Added internal research README  

---

## v1.0 — Genesis Prototype
**Date:** November 2025  

- Initial prototype demonstrating autonomous code mutation  
- Implemented basic mutation, evaluation, and scoring  
- Introduced early seeds: `sum_list`, `reverse_string`, `is_prime`  
- Produced first working evolutionary runs  
- Output logged to `results/vyktor_summary.json`

---


> “Evolution is not written — it is discovered.”  
> — NERON Research Division, 2025
