"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: scheduler.py  |  Module: Vyktor Evolution Scheduler (v1.2)
"""
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from . import mutate, evaluate

def _eval_candidate(cand, timeout=1.0):
    cand.evaluate(timeout=timeout)
    return cand

def evolve(task_name, seed_code, rounds=80, pop_size=12, timeout=1.0, max_workers=None):
    print(f"\n⚙️  Evolving {task_name} ...")
    pool = [evaluate.Candidate(seed_code, "seed")]
    for _ in range(pop_size - 1):
        pool.append(evaluate.Candidate(mutate.mutate_ast(seed_code), "init_mut"))

    best = None
    for r in range(rounds):
        to_eval = [c for c in pool if c.score == 0.0]
        if to_eval:
            with ProcessPoolExecutor(max_workers=max_workers) as ex:
                futures = {ex.submit(_eval_candidate, c, timeout): c for c in to_eval}
                for _ in as_completed(futures):
                    pass

        pool.sort(key=lambda x: x.score, reverse=True)

        if best is None or pool[0].score > best.score:
            best = pool[0]
            print(f"[Gen {r:02}] Best Score={best.score:.3f} | OK={best.ok} | RT={best.runtime:.3f}s | Origin={best.origin}")

        # survivors: top 3 (avoid pure seed dominance after early gens)
        survivors = []
        for c in pool:
            if r <= 5 or c.origin != "seed":
                survivors.append(c)
            if len(survivors) == 3:
                break
        if len(survivors) < 3:
            survivors = pool[:3]

        # reproduce (mutations; crossover planned next)
        new_pool = survivors.copy()
        while len(new_pool) < pop_size:
            parent = random.choice(survivors)
            child = evaluate.Candidate(mutate.mutate_ast(parent.code), origin=f"mut({parent.origin})")
            new_pool.append(child)
        pool = new_pool

    pool.sort(key=lambda x: x.score, reverse=True)
    return best, pool
