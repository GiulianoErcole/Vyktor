#!/usr/bin/env python3
"""
VYKTOR v1.0 — Self-Improving Code Evolution Engine
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
  ╚═══╝   ╚═════╝ ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
         Self-Improving Code Evolution Engine
"""

def main():
    print(BANNER)
    random.seed(time.time())

    seeds = synth.load_seed_tasks("data/seeds")
    results = {}

    for task_name, code in seeds.items():
        print(f"\n🧬 Beginning evolution: {task_name}")
        best = scheduler.evolve(task_name, code, rounds=40, pop_size=8)

        archive.save_candidate(task_name, best)
        results[task_name] = {
            "score": best.score,
            "ok": best.ok,
            "runtime": best.runtime,
            "origin": best.origin,
        }

    with open("results/vyktor_summary.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n🔬 Summary saved to results/vyktor_summary.json")

if __name__ == "__main__":
    os.makedirs("results/runs", exist_ok=True)
    main()
