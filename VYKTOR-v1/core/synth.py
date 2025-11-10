"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: synth.py  |  Module: Vyktor Seed Loader
"""

import os

def load_seed_tasks(path: str):
    seeds = {}
    for fn in os.listdir(path):
        if fn.endswith(".py"):
            with open(os.path.join(path, fn), "r", encoding="utf-8") as f:
                seeds[fn.replace(".py", "")] = f.read()
    return seeds
