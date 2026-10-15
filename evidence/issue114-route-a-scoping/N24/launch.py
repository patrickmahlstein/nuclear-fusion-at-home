"""Run arms sequentially, each in its own process group, killed at the 1.5 h wall budget."""
import os, signal, subprocess, sys, time
py, here = sys.argv[1], os.path.dirname(os.path.abspath(__file__))
sel = sys.argv[2]
for arm in sys.argv[3:] or ("nae3", "nae2", "sel401"):
    out = os.path.join(here, arm); os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "stdout.log"), "w") as log:
        p = subprocess.Popen([py, os.path.join(here, "run_arm.py"), arm, out, sel], stdout=log, stderr=subprocess.STDOUT,
                             start_new_session=True, env=dict(os.environ, PYTHONPATH=here))
        t = time.time()
        while p.poll() is None and time.time()-t < 5400: time.sleep(10)
        if p.poll() is None:
            log.write("\nKILLED at wall budget\n")
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try: os.killpg(p.pid, sig)
                except (ProcessLookupError, PermissionError): pass
                time.sleep(5)
        print(arm, "exit", p.poll(), "wall", round(time.time()-t), flush=True)
