## v1.3.1 — Seed Expansion (FULL)
- Integrated research-grade seeds: Huffman, LZ77, DPCM, Rabin–Karp, Bloom Filter, Karger Min-Cut,
  K-Means, TSP (SA), Symbolic Regression.
- Engine: same as v1.3.0-DEV (Trident, PATCH3) with telemetry + stable dashboard.

## v1.3.0-DEV — Trident (PATCH1)
- Fixed server global/port state; added /api/ports and reconnection logic
- Forced immediate evaluation → visible gen0 tick
- Lower default timeouts and rounds for snappier feedback
- Added 'seeds_loaded' event so dashboard is never idle at start
