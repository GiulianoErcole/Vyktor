# VYKTOR v1.1 — NERON Intelligence Systems (Internal)

**Tagline:** *It doesn’t write code — it evolves it.*

This version upgrades v1.0 with:
- ✅ Zero-dependency AST mutate (uses `ast.unparse` when available; no `astor` required).
- ✅ Stronger scoring (favor faster + smaller programs).
- ✅ Top-K archival for each task (best 5 saved in `results/runs`).
- ✅ Larger search by default (rounds=80, population=12).
- ✅ New seeds: `roman_to_int`, `levenshtein`, `lru_cache`.

## Quickstart
```bash
python3 vyktor.py
```

Artifacts appear under `results/runs/` and `results/vyktor_summary.json`.

## Add your own task
Add a new `*.py` into `data/seeds/` with a `solution()` and `run_tests()` function.
VYKTOR will discover it automatically.

---

© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
Unauthorized reproduction, distribution, or modification is strictly prohibited.
