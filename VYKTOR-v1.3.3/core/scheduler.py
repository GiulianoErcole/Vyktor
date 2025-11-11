import random, json, os, statistics
from concurrent.futures import ProcessPoolExecutor, as_completed
from . import mutate, evaluate, telemetry, fitness, seed_adapter

LOG_PATH = "results/live_feed.log"

def log_event(event):
    os.makedirs("results", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f: f.write(json.dumps(event) + "\n")

def dominates(a, b):
    a_ok, a_rt, a_len = a.fitness_vector(); b_ok, b_rt, b_len = b.fitness_vector()
    cond = (a_ok >= b_ok) and (a_rt <= b_rt) and (a_len <= b_len)
    strict = (a_ok > b_ok) or (a_rt < b_rt) or (a_len < b_len)
    return cond and strict

def pareto_fronts(pop):
    S = {i: [] for i in range(len(pop))}; n = [0]*len(pop); fronts=[[]]
    for i in range(len(pop)):
        for j in range(len(pop)):
            if i==j: continue
            if dominates(pop[i], pop[j]): S[i].append(j)
            elif dominates(pop[j], pop[i]): n[i]+=1
        if n[i]==0: fronts[0].append(i)
    k=0
    while fronts[k]:
        nxt=[]
        for i in fronts[k]:
            for j in S[i]:
                n[j]-=1
                if n[j]==0: nxt.append(j)
        k+=1; fronts.append(nxt)
    return [[pop[i] for i in fr] for fr in fronts if fr]

def crowding_distance(front):
    if not front: return {}
    dist={id(c):0.0 for c in front}
    triples=[(1 if c.ok else 0, c.runtime, len(c.code), c) for c in front]
    for idx, rev in [(0,True),(1,False),(2,False)]:
        triples.sort(key=lambda t: t[idx], reverse=rev)
        dist[id(triples[0][3])]=float('inf'); dist[id(triples[-1][3])]=float('inf')
        vmin=triples[0][idx]; vmax=triples[-1][idx]; rng=(vmax-vmin) or 1.0
        for i in range(1,len(triples)-1):
            prev=triples[i-1][idx]; nxt=triples[i+1][idx]; dist[id(triples[i][3])]+= (nxt-prev)/rng
    return dist

def select_survivors_pareto(pop, k):
    fronts = pareto_fronts(pop); survivors=[]
    for fr in fronts:
        if len(survivors)+len(fr) <= k: survivors.extend(fr)
        else:
            cd=crowding_distance(fr)
            survivors.extend(sorted(fr, key=lambda c: cd.get(id(c),0.0), reverse=True)[:(k-len(survivors))]); break
    return survivors[:k]

def _eval_candidate(cand, timeout=1.0):
    cand.evaluate(timeout=timeout); return cand

def evolve(task_name, seed_code, rounds=30, pop_size=12, timeout=0.3, max_workers=None, cfg=None, session_id=None, seed_path=None):
    cfg = cfg or {}; evo = cfg.get("evolution", {}); band = cfg.get("bandits", {})
    survivors_k=int(evo.get("survivors",5)); tmin=float(evo.get("timeout_scale_min",0.7)); tmax=float(evo.get("timeout_scale_max",1.2))
    objective=evo.get("objective","pareto"); bandits_on=bool(band.get("enabled",True)); eps=float(band.get("epsilon",0.10)); lr=float(band.get("lr",0.05))

    log_event({"task": task_name, "event": "task_start", "gen": -1, "objective": objective, "bandits": bandits_on})

    pool=[evaluate.Candidate(seed_code,"seed")] + [evaluate.Candidate(mutate.mutate_ast(seed_code, cfg),"init_mut") for _ in range(pop_size-1)]
    best=None; hist_runtimes=[]; op_weights={op:1.0 for op in ["binop","compare","const","for_step"]}

    # Immediate evaluation for visible gen0 tick
    try:
        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            futs = [ex.submit(_eval_candidate, c, timeout) for c in pool]
            out = []
            for f in as_completed(futs):
                try:
                    out.append(f.result())
                except Exception as e:
                    log_event({"task":task_name,"gen":0,"event":"eval_error","error":str(e)})
            if len(out)==len(pool):
                pool = out
    except Exception as e:
        log_event({"task":task_name,"gen":0,"event":"executor_error","error":str(e)})

    pool.sort(key=lambda x: x.score, reverse=True)
    if pool:
        best = pool[0]
        # Load optional fitness profile from seed file
        profile = {}
        try:
            if seed_path:
                mod = seed_adapter.load_seed_module(seed_path)
                profile = seed_adapter.get_fitness_profile(mod)
        except Exception:
            profile = {}

        oks = sum(1 for c in pool if c.ok)
        ok_rate = oks/float(len(pool))
        avg_runtime = (sum(c.runtime for c in pool)/len(candidates)) if (candidates:=pool) else 0.0
        hist_runtimes.extend([c.runtime for c in pool])
        log_event({"task":task_name,"event":"gen_tick","gen":0,"score":fitness.combine(getattr(best,'metrics',{}), profile),"ok":best.ok,"runtime":best.runtime,"origin":best.origin,"ok_rate":ok_rate,"avg_runtime":avg_runtime})
        if session_id is not None:
            telemetry.record_generation(session_id, task_name, 0, ok_rate, avg_runtime, best.score, bandit={"weights":op_weights})

    # Main loop
    for r in range(1, rounds):
        if hist_runtimes:
            avg_rt = statistics.mean(hist_runtimes[-min(len(hist_runtimes),10):])
            cur_timeout = max(timeout*tmin, min(timeout*tmax, avg_rt*2.0))
        else:
            cur_timeout = timeout

        to_eval=[i for i,c in enumerate(pool) if c.score==0.0]
        if to_eval:
            with ProcessPoolExecutor(max_workers=max_workers) as ex:
                fut_to_idx={ex.submit(_eval_candidate, pool[i], cur_timeout): i for i in to_eval}
                for fut in as_completed(fut_to_idx):
                    i=fut_to_idx[fut]
                    try:
                        pool[i]=fut.result(); hist_runtimes.append(pool[i].runtime)
                    except Exception as e:
                        bad=pool[i]; bad.ok=False; bad.runtime=cur_timeout; bad.score=0.0; log_event({"task":task_name,"gen":r,"event":"eval_error","error":str(e)})

        if objective=="pareto":
            survivors=select_survivors_pareto(pool, survivors_k)
            if survivors:
                top_candidate=max(survivors, key=lambda c:c.score)
                if best is None or top_candidate.score>best.score: best=top_candidate
        else:
            pool.sort(key=lambda x:x.score, reverse=True); survivors=pool[:survivors_k]
            if best is None or (pool and pool[0].score>best.score): best=pool[0]

        oks=sum(1 for c in pool if c.ok); ok_rate=oks/float(len(pool)) if pool else 0.0
        avg_runtime=statistics.mean([c.runtime for c in pool]) if pool else 0.0
        top = best if best else (pool[0] if pool else None)
        log_event({"task":task_name,"event":"gen_tick","gen":r,"score":(fitness.combine(getattr(top,'metrics',{}), profile) if top else 0.0),"ok":(top.ok if top else False),"runtime":(top.runtime if top else 0.0),"origin":(top.origin if top else "seed"),"ok_rate":ok_rate,"avg_runtime":avg_runtime,"bandit":{"weights":op_weights}})
        if session_id is not None and top is not None:
            telemetry.record_generation(session_id, task_name, r, ok_rate, avg_runtime, top.score, bandit={"weights":op_weights})

        new_pool=survivors.copy()
        while len(new_pool)<pop_size:
            parent=random.choice(survivors) if survivors else random.choice(pool)
            op=max(op_weights,key=op_weights.get) if (bandits_on and random.random()>eps) else random.choice(list(op_weights.keys()))
            child_code=mutate.mutate_ast(parent.code, cfg, force_op=op); child=evaluate.Candidate(child_code, origin=f"mut-{op}({parent.origin})")
            new_pool.append(child)

        for op in op_weights:
            appear=sum(1 for c in survivors if f"mut-{op}" in c.origin)
            op_weights[op]=max(0.05, op_weights[op]*(1.0-lr)+lr*(0.5+0.1*appear))

        pool=new_pool

    if objective=="pareto":
        final_surv=select_survivors_pareto(pool, max(1, survivors_k))
        best=max(final_surv, key=lambda c:c.score) if final_surv else best
    else:
        pool.sort(key=lambda x:x.score, reverse=True); best=pool[0]
    log_event({"task":task_name,"event":"complete","best_score":(best.score if best else 0.0)})
    pool.sort(key=lambda x:x.score, reverse=True)
    return best, pool
