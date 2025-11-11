import os, subprocess, tempfile, sys, time
class Candidate:
    def __init__(self, code: str, origin: str):
        self.code = code; self.origin = origin
        self.score = 0.0; self.ok = False; self.runtime = 0.0
    def evaluate(self, timeout=1.0):
        ok, out, rt = sandbox_exec(self.code, timeout)
        self.ok = ok; self.runtime = rt
        length_penalty = 0.0002 * len(self.code)
        speed_penalty  = 0.05 * min(rt, timeout)
        novelty_bonus  = 0.01 if self.origin != "seed" else 0.0
        self.score = (1 if ok else 0) - speed_penalty - length_penalty + novelty_bonus
        return ok, out, rt
    def fitness_vector(self):
        return (1 if self.ok else 0, self.runtime, len(self.code))
def sandbox_exec(code: str, timeout=1.0):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(code); path = tf.name
    start = time.time()
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        elapsed = time.time() - start; ok = proc.returncode == 0; output = proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start; ok = False; output = f"TIMEOUT ({timeout}s)"
    finally:
        try: os.unlink(path)
        except Exception: pass
    return ok, output.strip(), elapsed
