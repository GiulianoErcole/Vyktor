#!/usr/bin/env python3
"""
VYKTOR v1.2-dev — Self-Improving Code Evolution Engine
"It doesn’t write code — it evolves it."

© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
Unauthorized reproduction, distribution, or modification is strictly prohibited.
"""

import os, json, random
from core import mutate, evaluate, synth, scheduler, archive, gene_pool

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
    random.seed(1337)  # deterministic runs
    gene_pool.init()

    seeds_map = synth.load_seed_tasks("data/seeds")
    results = {}

    for task_name, code in seeds_map.items():
        print(f"\n🧬 Beginning evolution: {task_name}")
        best, sorted_pool = scheduler.evolve(
            task_name, code,
            rounds=80, pop_size=12,
            timeout=1.0,
            max_workers=os.cpu_count()  # parallelize across cores
        )
        archive.save_candidate(task_name, best)
        archive.save_topk(task_name, sorted_pool, k=5)

        # persist into gene pool
        gene_pool.add(task_name, best)
        for c in sorted_pool[:5]:
            gene_pool.add(task_name, c)

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
