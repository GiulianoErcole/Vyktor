import os, subprocess, tempfile, time
IMAGE = os.environ.get("VYKTOR_DOCKER_IMAGE", "vyktor-sandbox:latest")
def docker_exec(code: str, timeout=1.0):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(code); path=tf.name
    start=time.time()
    try:
        cmd=["docker","run","--rm","-m","128m","--cpus","0.5","-v",f"{path}:/tmp/cand.py:ro",IMAGE,"/tmp/cand.py"]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout+0.5)
        ok=p.returncode==0; output=p.stdout+p.stderr
    except subprocess.TimeoutExpired:
        ok=False; output=f"TIMEOUT ({timeout}s)"
    finally:
        try: os.unlink(path)
        except: pass
    return ok, output.strip(), time.time()-start
