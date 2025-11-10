"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: archive.py  |  Module: Vyktor Archive System
"""

import os, json

def save_candidate(task_name, candidate):
    os.makedirs("results/runs", exist_ok=True)
    out_code = f"results/runs/vyktor_best_{task_name}.py"
    out_meta = f"results/runs/vyktor_best_{task_name}.json"
    with open(out_code, "w", encoding="utf-8") as f:
        f.write(candidate.code)
    meta = {"score": candidate.score, "ok": candidate.ok, "runtime": candidate.runtime, "origin": candidate.origin}
    with open(out_meta, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"📦 Saved best candidate for {task_name} -> {out_code}")

def save_topk(task_name, candidates, k=5):
    os.makedirs("results/runs", exist_ok=True)
    for i, c in enumerate(candidates[:k], 1):
        with open(f"results/runs/{task_name}_top{i}.py", "w", encoding="utf-8") as f:
            f.write(c.code)
        with open(f"results/runs/{task_name}_top{i}.json", "w", encoding="utf-8") as f:
            json.dump({"score": c.score, "ok": c.ok, "runtime": c.runtime, "origin": c.origin}, f, indent=2)
