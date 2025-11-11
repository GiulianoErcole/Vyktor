import importlib.util, types, os, json

def load_seed_module(path: str) -> types.ModuleType | None:
    try:
        spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return mod
    except Exception as e:
        return None

def get_fitness_profile(mod) -> dict:
    return getattr(mod, "FITNESS_PROFILE", {}) if mod else {}

def run_tests(mod) -> tuple[bool, dict]:
    # Basic contract: mod.run_tests() should raise on failure
    metrics = {}
    ok = False
    try:
        if hasattr(mod, "run_tests"):
            mod.run_tests()
            ok = True
        # Seeds may optionally expose quick metrics probe
        if hasattr(mod, "fitness_probe"):
            # must return a dict
            m = mod.fitness_probe()
            if isinstance(m, dict):
                metrics.update(m)
    except Exception:
        ok = False
    metrics["ok"] = 1.0 if ok else 0.0
    return ok, metrics
