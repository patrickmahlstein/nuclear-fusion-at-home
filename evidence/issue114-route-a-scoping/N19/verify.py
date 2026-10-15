"""N19 verification: nonlinear solves at dx/2, dx, 2dx (prereg), mirror metrics only."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import fd
step = json.load(open(sys.argv[1])); fd.OUT = sys.argv[2]
with open(sys.argv[2], "a") as fh:
    for scale in (0.5, 1.0, 2.0):
        mods = [((k, m, n), scale*d) for (k, m, n), d in zip(step["modes"], step["dx"])]
        r = fd.solve(mods, f"step{scale}")
        fh.write(json.dumps(dict(tag=f"step{scale}", scale=scale, **r)) + "\n"); fh.flush()
