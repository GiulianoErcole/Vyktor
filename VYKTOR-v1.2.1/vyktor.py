#!/usr/bin/env python3
"""
VYKTOR v1.2.1 - Self-Improving Code Evolution Engine
"It doesn't write code — it evolves it."

(c) 2025 NERON Intelligence Systems - Internal Experimental Research Prototype.
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
    random.seed(1337)
    os.makedirs("results", exist_ok=True)
    open("results/live_feed.log", "w", encoding="utf-8").close()

    gene_pool.init()
    seeds_map = synth.load_seed_tasks("data/seeds")
    summary = {}

    for task_name, code in seeds_map.items():
        print(f"\n🧬 Beginning evolution: {task_name}")
        best, sorted_pool = scheduler.evolve(
            task_name, code,
            rounds=80, pop_size=12,
            timeout=1.0,
            max_workers=os.cpu_count()
        )
        archive.save_candidate(task_name, best)
        archive.save_topk(task_name, sorted_pool, k=5)

        gene_pool.add(task_name, best)
        for c in sorted_pool[:5]:
            gene_pool.add(task_name, c)

        summary[task_name] = {
            "score": best.score,
            "ok": best.ok,
            "runtime": best.runtime,
            "origin": best.origin,
        }

    with open("results/vyktor_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print("\nSummary saved to results/vyktor_summary.json")

if __name__ == "__main__":
    os.makedirs("results/runs", exist_ok=True)
    main()
