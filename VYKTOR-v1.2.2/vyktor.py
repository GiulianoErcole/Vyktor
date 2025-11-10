#!/usr/bin/env python3
import os, json, random
from core import mutate, evaluate, synth, scheduler, archive, gene_pool
def main():
    random.seed(1337)
    os.makedirs("results", exist_ok=True)
    with open("results/live_feed.log", "w", encoding="utf-8") as lf:
        lf.write('{"event":"session_start"}\n')
    gene_pool.init()
    seeds_map = synth.load_seed_tasks("data/seeds")
    summary = {}
    for task_name, code in seeds_map.items():
        best, sorted_pool = scheduler.evolve(task_name, code, rounds=80, pop_size=12, timeout=1.0, max_workers=os.cpu_count())
        archive.save_candidate(task_name, best)
        archive.save_topk(task_name, sorted_pool, k=5)
        gene_pool.add(task_name, best)
        for c in sorted_pool[:5]: gene_pool.add(task_name, c)
        summary[task_name] = {"score": best.score, "ok": best.ok, "runtime": best.runtime, "origin": best.origin}
    with open("results/vyktor_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
if __name__ == "__main__":
    os.makedirs("results/runs", exist_ok=True)
    main()
