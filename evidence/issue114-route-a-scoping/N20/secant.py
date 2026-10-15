"""N20 step 1: large-step secant sensitivities on low-order modes around N19's dx boundary."""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "n19"))
import fd
from metrics2 import metrics
fd.metrics = metrics
step = json.load(open(sys.argv[1])); OUT = sys.argv[2]; fd.OUT = OUT
start = [((k, m, n), d) for (k, m, n), d in zip(step["modes"], step["dx"])]
low = [tuple(md) for md in step["modes"] if md[1] <= 3 and abs(md[2]) <= 3]
checks = [("rbc", 1, 0), ("rbc", 2, 0), ("zbs", 1, 1), ("zbs", 2, -2)]
jobs = [("start", [], None, 0)] + [(f"{k}{m}_{n}", [((k, m, n), 5e-3)], (k, m, n), 5e-3) for k, m, n in low] \
     + [(f"{k}{m}_{n}_h2.5e-3", [((k, m, n), 2.5e-3)], (k, m, n), 2.5e-3) for k, m, n in checks]
t0 = time.time()
with open(OUT, "a") as fh:
    for tag, mods, mode, h in jobs:
        if time.time()-t0 > 3600: fh.write(json.dumps(dict(stopped="budget"))+"\n"); break
        r = fd.solve(start + mods, tag)
        fh.write(json.dumps(dict(tag=tag, mode=mode, h=h, **r))+"\n"); fh.flush()
