import os

def load_seed_tasks(path: str):
    seeds={}
    for fn in os.listdir(path):
        if fn.endswith('.py'):
            full=os.path.join(path, fn)
            with open(full,'r',encoding='utf-8') as f:
                seeds[fn.replace('.py','')]={'code':f.read(),'path':full}
    return seeds
