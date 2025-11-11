import os, json
def save_candidate(task_name, candidate):
    os.makedirs("results/runs", exist_ok=True)
    with open(f"results/runs/vyktor_best_{task_name}.py","w",encoding="utf-8") as f: f.write(candidate.code)
    with open(f"results/runs/vyktor_best_{task_name}.json","w",encoding="utf-8") as f: json.dump({"score":candidate.score,"ok":candidate.ok,"runtime":candidate.runtime,"origin":candidate.origin}, f, indent=2)
def save_topk(task_name, candidates, k=6):
    os.makedirs("results/runs", exist_ok=True)
    for i,c in enumerate(candidates[:k],1):
        with open(f"results/runs/{task_name}_top{i}.py","w",encoding="utf-8") as f: f.write(c.code)
        with open(f"results/runs/{task_name}_top{i}.json","w",encoding="utf-8") as f: json.dump({"score":c.score,"ok":c.ok,"runtime":c.runtime,"origin":c.origin}, f, indent=2)
