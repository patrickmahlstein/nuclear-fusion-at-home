"""N34: Poincare section (phi=0) of the selected401 fit for launches across s 0.44-0.56 (theta=0), 200 transits."""
import json, math, sys
import numpy as np
SNAP, WOUT, M28, OUT = sys.argv[1:5]
sys.argv = [sys.argv[0], SNAP, WOUT, "/dev/null"]
src = open(M28).read().split("cases = [(s, th)")[0]; g = {}; exec(compile(src, M28, "exec"), g)
sig = np.linspace(0.44, 0.58, 16)
pts = g["trace"]([g["rz"](float(s), 0.0) for s in sig], 200, 1e-10)
res = [dict(sigma=float(s), n=len(p), s_real=g["flux_of"](p, g["axis"])[0]/g["flux_edge"], rz=p.tolist()) for s, p in zip(sig, pts)]
json.dump(dict(axis=list(g["axis"]), lines=res), open(OUT + ".json", "w"))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
for r in res:
    p = np.array(r["rz"]); ax[0].plot(p[:, 0], p[:, 1], ".", ms=1.5)
    ang = np.arctan2(p[:, 1]-g["axis"][1], p[:, 0]-g["axis"][0]); rad = np.hypot(p[:, 0]-g["axis"][0], p[:, 1]-g["axis"][1])
    ax[1].plot(ang, rad, ".", ms=1.5)
ax[0].set_aspect("equal"); ax[0].set_title("phi=0 crossings"); ax[1].set_title("angle about axis vs distance"); fig.savefig(OUT + ".png", dpi=110)
for r in res: print(round(r["sigma"], 4), round(r["s_real"], 4), r["n"])
