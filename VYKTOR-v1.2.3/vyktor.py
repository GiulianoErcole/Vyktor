#!/usr/bin/env python3
import os, json, random
from core import mutate, evaluate, synth, scheduler, archive, gene_pool, telemetry
def main():
    cfg = json.load(open("config.json")) if os.path.exists("config.json") else {}
    random.seed(1337)
    os.makedirs("results", exist_ok=True)
    with open("results/live_feed.log", "w", encoding="utf-8") as lf:
        lf.write('{"event":"session_start","version":"1.2.3"}\n')
    gene_pool.init(); telemetry.init_db()
    session_id = telemetry.start_session(meta={"version":"1.2.3"})
    seeds_map = synth.load_seed_tasks("data/seeds")
    summary = {}
    rounds = cfg.get("evolution", {}).get("rounds", 80)
    pop_size = cfg.get("evolution", {}).get("pop_size", 12)
    base_timeout = cfg.get("evolution", {}).get("base_timeout", 1.0)
    for task_name, code in seeds_map.items():
        best, sorted_pool = scheduler.evolve(task_name, code, rounds=rounds, pop_size=pop_size, timeout=base_timeout, max_workers=os.cpu_count(), cfg=cfg, session_id=session_id)
        archive.save_candidate(task_name, best); archive.save_topk(task_name, sorted_pool, k=5)
        gene_pool.add(task_name, best); [gene_pool.add(task_name, c) for c in sorted_pool[:5]]
        summary[task_name] = {"score": best.score, "ok": best.ok, "runtime": best.runtime, "origin": best.origin}
    with open("results/vyktor_summary.json", "w", encoding="utf-8") as f: json.dump(summary, f, indent=2)
    telemetry.end_session(session_id, summary=summary)
if __name__ == "__main__":
    os.makedirs("results/runs", exist_ok=True); main()
