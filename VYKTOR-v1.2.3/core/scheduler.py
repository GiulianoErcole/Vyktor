import random, json, os, statistics
from concurrent.futures import ProcessPoolExecutor, as_completed
from . import mutate, evaluate, telemetry
LOG_PATH = "results/live_feed.log"
def log_event(event):
    os.makedirs("results", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f: f.write(json.dumps(event) + "\n")
def _eval_candidate(cand, timeout=1.0):
    cand.evaluate(timeout=timeout); return cand
def evolve(task_name, seed_code, rounds=80, pop_size=12, timeout=1.0, max_workers=None, cfg=None, session_id=None):
    cfg = cfg or {}; evo = cfg.get("evolution", {})
    survivors_k = int(evo.get("survivors", 3)); tmin = float(evo.get("timeout_scale_min", 0.75)); tmax = float(evo.get("timeout_scale_max", 1.50))
    log_event({"task": task_name, "event": "task_start", "gen": -1})
    pool = [evaluate.Candidate(seed_code, "seed")] + [evaluate.Candidate(mutate.mutate_ast(seed_code, cfg), "init_mut") for _ in range(pop_size-1)]
    best = None; hist_runtimes = []
    for r in range(rounds):
        if hist_runtimes:
            avg_rt = statistics.mean(hist_runtimes[-min(len(hist_runtimes),10):]); cur_timeout = max(timeout*tmin, min(timeout*tmax, avg_rt*2.0))
        else: cur_timeout = timeout
        to_eval_idx = [i for i,c in enumerate(pool) if c.score == 0.0]
        if to_eval_idx:
            with ProcessPoolExecutor(max_workers=max_workers) as ex:
                fut_to_idx = {ex.submit(_eval_candidate, pool[i], cur_timeout): i for i in to_eval_idx}
                for fut in as_completed(fut_to_idx):
                    i = fut_to_idx[fut]
                    try: pool[i] = fut.result(); hist_runtimes.append(pool[i].runtime)
                    except Exception as e:
                        bad = pool[i]; bad.ok=False; bad.runtime=cur_timeout; bad.score=0.0; log_event({"task": task_name, "gen": r, "event": "eval_error", "error": str(e)})
        pool.sort(key=lambda x: x.score, reverse=True)
        if best is None or pool[0].score > best.score: best = pool[0]
        oks = sum(1 for c in pool if c.ok); ok_rate = oks/float(len(pool)); avg_runtime = statistics.mean([c.runtime for c in pool]) if pool else 0.0
        log_event({"task": task_name, "event": "gen_tick", "gen": r, "score": pool[0].score, "ok": pool[0].ok, "runtime": pool[0].runtime, "origin": pool[0].origin, "ok_rate": ok_rate, "avg_runtime": avg_runtime})
        if session_id is not None: telemetry.record_generation(session_id, task_name, r, ok_rate, avg_runtime, pool[0].score)
        survivors = pool[:survivors_k]; new_pool = survivors.copy()
        while len(new_pool) < pop_size:
            parent = random.choice(survivors); child = evaluate.Candidate(mutate.mutate_ast(parent.code, cfg), origin=f"mut({parent.origin})"); new_pool.append(child)
        pool = new_pool
    pool.sort(key=lambda x: x.score, reverse=True); log_event({"task": task_name, "event": "complete", "best_score": pool[0].score}); return pool[0], pool
