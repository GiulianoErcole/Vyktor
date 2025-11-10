"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: evaluate.py  |  Module: Vyktor Core
"""

import subprocess, tempfile, os, sys, time

class Candidate:
    def __init__(self, code: str, origin: str):
        self.code = code
        self.origin = origin
        self.score = 0.0
        self.ok = False
        self.runtime = 0.0

    def evaluate(self, timeout=1.0):
        ok, out, rt = sandbox_exec(self.code, timeout)
        self.ok = ok
        self.runtime = rt
        self.score = (1 if ok else 0) - 0.01 * rt
        return ok, out, rt

def sandbox_exec(code: str, timeout=1.0):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(code)
        path = tf.name
    start = time.time()
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        elapsed = time.time() - start
        ok = proc.returncode == 0
        output = proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        ok = False
        output = f"TIMEOUT ({timeout}s)"
    finally:
        try: os.unlink(path)
        except Exception: pass
    return ok, output.strip(), elapsed
