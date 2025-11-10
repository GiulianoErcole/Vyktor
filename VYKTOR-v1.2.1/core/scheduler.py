import random, json, os
from concurrent.futures import ProcessPoolExecutor, as_completed
from . import mutate, evaluate

LOG_PATH = "results/live_feed.log"

def log_event(event):
    os.makedirs("results", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

def _eval_candidate(cand, timeout=1.0):
    cand.evaluate(timeout=timeout)
    return cand

def evolve(task_name, seed_code, rounds=80, pop_size=12, timeout=1.0, max_workers=None):
    print(f"\nEvolving {task_name} ...")
    pool = [evaluate.Candidate(seed_code, "seed")]
    for _ in range(pop_size - 1):
        pool.append(evaluate.Candidate(mutate.mutate_ast(seed_code), "init_mut"))
    best = None
    for r in range(rounds):
        to_eval_idx = [i for i, c in enumerate(pool) if c.score == 0.0]
        if to_eval_idx:
            with ProcessPoolExecutor(max_workers=max_workers) as ex:
                fut_to_idx = {ex.submit(_eval_candidate, pool[i], timeout): i for i in to_eval_idx}
                for fut in as_completed(fut_to_idx):
                    i = fut_to_idx[fut]
                    try:
                        pool[i] = fut.result()
                    except Exception as e:
                        bad = pool[i]
                        bad.ok = False; bad.runtime = timeout; bad.score = 0.0
                        log_event({"task": task_name, "gen": r, "event": "eval_error", "error": str(e)})
        pool.sort(key=lambda x: x.score, reverse=True)
        if best is None or pool[0].score > best.score:
            best = pool[0]
            print(f"[Gen {r:02}] Best Score={best.score:.3f} | OK={best.ok} | RT={best.runtime:.3f}s | Origin={best.origin}")
            log_event({"task": task_name, "gen": r, "score": best.score, "ok": best.ok, "runtime": best.runtime, "origin": best.origin})
        survivors = pool[:3]
        new_pool = survivors.copy()
        while len(new_pool) < pop_size:
            parent = random.choice(survivors)
            child = evaluate.Candidate(mutate.mutate_ast(parent.code), origin=f"mut({parent.origin})")
            new_pool.append(child)
        pool = new_pool
    pool.sort(key=lambda x: x.score, reverse=True)
    log_event({"task": task_name, "event": "complete", "best_score": best.score})
    return best, pool
