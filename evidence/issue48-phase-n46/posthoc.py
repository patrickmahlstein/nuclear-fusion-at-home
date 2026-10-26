"""N46 post-hoc diagnostic (after the preregistered result): metric B with an alias-free rotation estimate.
Rotation = the iota in (0,1) whose frac(k*iota) ordering gives the shortest closed polyline (grid 1e-4, then 1e-7)."""
import json, numpy as np
def seg_dist(x, a, b):
    ab = b-a; t = np.clip(np.einsum("ij,kij->ki", ab, x[:, None, :]-a[None]) / np.maximum(np.sum(ab*ab, 1), 1e-300), 0, 1)
    proj = a[None]+t[..., None]*ab[None]; return np.min(np.hypot(*(x[:, None, :]-proj).transpose(2, 0, 1)), axis=1)
def perim(p, i):
    c = p[np.argsort(np.mod(np.arange(len(p))*i, 1.0))]; return np.sum(np.hypot(*(np.roll(c, -1, 0)-c).T))
def rot(p):
    g = np.arange(1e-4, 1, 1e-4); best = g[np.argmin([perim(p, i) for i in g])]
    f = np.linspace(best-2e-4, best+2e-4, 4001); return float(f[np.argmin([perim(p, i) for i in f])])
out = {}
for s in ("0.5", "0.75"):
    z = np.load(f"result.json.s{s}.npz"); P = [z[k] for k in sorted(z.files, key=lambda k: int(k.split("_")[1]))]
    r = [rot(p) for p in P]
    poly = [(lambda c: (c, np.roll(c, -1, 0)))(p[np.argsort(np.mod(np.arange(len(p))*ri, 1.0))]) for p, ri in zip(P, r)]
    B = max(float(np.max(seg_dist(P[b], *poly[a]))) for a in range(4) for b in range(4) if a != b)
    out[s] = dict(rotation=r, rotation_spread=max(r)-min(r), B_mm=1e3*B)
    print(s, out[s])
json.dump(out, open("posthoc.json", "w"), indent=1)
