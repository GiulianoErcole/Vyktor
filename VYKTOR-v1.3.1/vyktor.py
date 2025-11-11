#!/usr/bin/env python3
import os, json, random, time
from core import mutate, evaluate, synth, scheduler, archive, gene_pool, telemetry
from core.scheduler import log_event

def banner():
    http = os.environ.get("HTTP_PORT","8080")
    print('\n==============================================================\n© 2025 NERON Intelligence Systems — VYKTOR v1.3.0 DEV (Trident)\nNeural Evolution Engine • Dashboard: http://127.0.0.1:{http}\n==============================================================\n'.format(http=http))

def main():
    cfg = json.load(open("config.json")) if os.path.exists("config.json") else {}
    random.seed(1337)
    os.makedirs("results", exist_ok=True)
    lf_path="results/live_feed.log"
    if os.path.exists(lf_path) and os.path.getsize(lf_path) > 2_000_000:
        ts=int(time.time()); os.replace(lf_path, f"results/live_feed_{ts}.log")
    with open(lf_path, "a", encoding="utf-8") as lf:
        lf.write('{"event":"session_start","version":"1.3.0-dev","ts":'+str(time.time())+'}\n')

    gene_pool.init(); telemetry.init_db()
    session_id = telemetry.start_session(meta={"version":"1.3.0-dev"})

    seeds_map = synth.load_seed_tasks("data/seeds")
    log_event({"event":"seeds_loaded","count":len(seeds_map),"tasks":list(seeds_map.keys())})

    summary = {}
    rounds = cfg.get("evolution",{}).get("rounds",30)
    pop_size = cfg.get("evolution",{}).get("pop_size",12)
    base_timeout = cfg.get("evolution",{}).get("base_timeout",0.3)

    for task_name, code in seeds_map.items():
        best, sorted_pool = scheduler.evolve(task_name, code, rounds=rounds, pop_size=pop_size,
                                             timeout=base_timeout, max_workers=os.cpu_count(),
                                             cfg=cfg, session_id=session_id)
        archive.save_candidate(task_name, best); archive.save_topk(task_name, sorted_pool, k=6)
        for c in sorted_pool[:6]: gene_pool.add(task_name, c)
        summary[task_name] = {"score": best.score, "ok": best.ok, "runtime": best.runtime, "origin": best.origin, "length": len(best.code)}

    with open("results/vyktor_summary.json","w",encoding="utf-8") as f: json.dump(summary, f, indent=2)
    telemetry.end_session(session_id, summary=summary)

if __name__ == "__main__":
    os.makedirs("results/runs", exist_ok=True)
    banner()
    main()
