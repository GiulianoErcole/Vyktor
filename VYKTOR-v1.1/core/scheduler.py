"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: scheduler.py  |  Module: Vyktor Evolution Scheduler
"""

import random
from . import mutate, evaluate

def evolve(task_name, seed_code, rounds=80, pop_size=12):
    print(f"\n⚙️  Evolving {task_name} ...")
    pool = [evaluate.Candidate(seed_code, "seed")]
    for _ in range(pop_size - 1):
        pool.append(evaluate.Candidate(mutate.mutate_ast(seed_code), "init_mut"))

    best = None
    for r in range(rounds):
        for c in pool:
            if c.score == 0.0:
                c.evaluate()
        pool.sort(key=lambda x: x.score, reverse=True)

        if best is None or pool[0].score > best.score:
            best = pool[0]
            print(f"[Gen {r:02}] Best Score={best.score:.3f} | OK={best.ok} | RT={best.runtime:.3f}s | Origin={best.origin}")

        survivors = pool[:3]
        new_pool = survivors.copy()
        while len(new_pool) < pop_size:
            parent = random.choice(survivors)
            child = evaluate.Candidate(mutate.mutate_ast(parent.code), f"mut({parent.origin})")
            new_pool.append(child)
        pool = new_pool
    pool.sort(key=lambda x: x.score, reverse=True)
    return best, pool
