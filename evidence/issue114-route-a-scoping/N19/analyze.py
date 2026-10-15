"""N19 analysis: Jacobian of (W, FC, A, iota/nfp) wrt boundary modes; least-norm step (prereg)."""
import json, sys, numpy as np
rows = [json.loads(l) for l in open(sys.argv[1])]
base = next(r for r in rows if r.get("tag") == "base")
keys = ("vacuum_well", "flux_compression", "aspect", "iota_edge_per_fp")
fd = [r for r in rows if r.get("mode") and r["h"] == 1e-3 and "error" not in r]
chk = {tuple(r["mode"]): r for r in rows if r.get("mode") and r["h"] == 5e-4 and "error" not in r}
J = np.array([[(r[k]-base[k])/r["h"] for k in keys] for r in fd]).T  # 4 x M
modes = [tuple(r["mode"]) for r in fd]
print("modes", len(modes), "failed", sum("error" in r for r in rows))
for k, row in zip(keys, J):
    top = np.argsort(-abs(row))[:6]
    print(k, [(modes[i], round(row[i], 3)) for i in top])
lin = {}
for m, r in chk.items():
    i = modes.index(m)
    lin[str(m)] = {k: (J[j, i], (r[k]-base[k])/5e-4) for j, k in enumerate(keys)}
print("step check (slope h=1e-3, h=5e-4):", json.dumps(lin, default=float)[:1500])
target = np.array([0.016+0.005-0.0, 0.9-base["flux_compression"]-0.05, 0.0, 0.0])
target[0] = 0.005 - base["vacuum_well"]
dx = np.linalg.lstsq(J, target, rcond=None)[0]
print("target", target, "|dx|", np.linalg.norm(dx), "max|dx|", abs(dx).max())
print("largest dx", [(modes[i], round(dx[i], 5)) for i in np.argsort(-abs(dx))[:10]])
json.dump(dict(modes=modes, dx=dx.tolist(), J=J.tolist(), target=target.tolist()), open(sys.argv[2], "w"))
