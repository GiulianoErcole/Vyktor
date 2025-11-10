#!/usr/bin/env python3
"""
VYKTOR v1.1 — Self-Improving Code Evolution Engine
"It doesn’t write code — it evolves it."

© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
Unauthorized reproduction, distribution, or modification is strictly prohibited.
"""

import os, json, random, time
from core import mutate, evaluate, synth, scheduler, archive

BANNER = r"""
██╗   ██╗██╗   ██╗██╗██╗  ██╗████████╗ ██████╗ ██████╗ 
██║   ██║██║   ██║██║██║ ██╔╝╚══██╔══╝██╔═══██╗██╔══██╗
██║   ██║██║   ██║██║█████╔╝    ██║   ██║   ██║██████╔╝
╚██╗ ██╔╝██║   ██║██║██╔═██╗    ██║   ██║   ██║██╔══██╗
 ╚████╔╝ ╚██████╔╝██║██║  ██╗   ██║   ╚██████╔╝██║  ██║
  ╚═══╝   ╚═════╝ ╚═╝╚═╝  ╚═╝   ╚═════╝ ╚═╝  ╚═╝
         Self-Improving Code Evolution Engine
"""

def main():
    print(BANNER)
    # Set a deterministic seed for reproducible runs; comment to randomize
    random.seed(1337)

    seeds = synth.load_seed_tasks("data/seeds")
    results = {}

    for task_name, code in seeds.items():
        print(f"\n🧬 Beginning evolution: {task_name}")
        best, sorted_pool = scheduler.evolve(task_name, code, rounds=80, pop_size=12)
        archive.save_candidate(task_name, best)
        archive.save_topk(task_name, sorted_pool, k=5)
        results[task_name] = {
            "score": best.score,
            "ok": best.ok,
            "runtime": best.runtime,
            "origin": best.origin,
        }

    os.makedirs("results", exist_ok=True)
    with open("results/vyktor_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\n🔬 Summary saved to results/vyktor_summary.json")

if __name__ == "__main__":
    os.makedirs("results/runs", exist_ok=True)
    main()
