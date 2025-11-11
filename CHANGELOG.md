# 🧬 VYKTOR — CHANGELOG
### © 2025 NERON Intelligence Systems  


### Next Planned

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
