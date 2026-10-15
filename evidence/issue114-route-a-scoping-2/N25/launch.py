"""N25: one ALM arm per dataset seed, each in its own process group, 1.5 h wall."""
import os, signal, subprocess, sys, time
py, here = sys.argv[1], os.path.dirname(os.path.abspath(__file__))
for row in sys.argv[2:]:
    out = os.path.join(here, f"row{row}"); os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "stdout.log"), "w") as log:
        p = subprocess.Popen([py, os.path.join(here, "run_arm.py"), f"row{row}", out, os.path.join(here, f"seed-{row}.json")],
                             stdout=log, stderr=subprocess.STDOUT, start_new_session=True, env=dict(os.environ, PYTHONPATH=here))
        t = time.time()
        while p.poll() is None and time.time()-t < 5400: time.sleep(10)
        if p.poll() is None:
            log.write("\nKILLED at wall budget\n")
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try: os.killpg(p.pid, sig)
                except (ProcessLookupError, PermissionError): pass
                time.sleep(5)
        print(row, "exit", p.poll(), "wall", round(time.time()-t), flush=True)
