"""
© 2025 NERON Intelligence Systems — Internal Experimental Research Prototype.
File: docker_backend.py  |  Module: Optional Docker Sandbox
"""
import os, subprocess, tempfile, time

IMAGE = os.environ.get("VYKTOR_DOCKER_IMAGE", "vyktor-sandbox:latest")

def docker_exec(code: str, timeout=1.0):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(code)
        path = tf.name
    start = time.time()
    try:
        cmd = ["docker", "run", "--rm", "-m", "128m", "--cpus", "0.5",
               "-v", f"{path}:/tmp/cand.py:ro", IMAGE, "/tmp/cand.py"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+0.5)
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
