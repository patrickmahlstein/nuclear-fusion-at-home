"""Post-hoc 2: s = 0.5 metric B with each line ordered by min-perimeter rotation restricted to (0, 0.5) (removes the
iota <-> 1-iota degeneracy), plus distance to the nearest rational p/q (q <= 20)."""
import json, numpy as np
from fractions import Fraction
exec(open("posthoc.py").read().split("out = {}")[0])
def rot_half(p):
    g = np.arange(1e-4, 0.5, 1e-4); best = g[np.argmin([perim(p, i) for i in g])]
    f = np.linspace(best-2e-4, best+2e-4, 4001); return float(f[np.argmin([perim(p, i) for i in f])])
z = np.load("result.json.s0.5.npz"); P = [z[k] for k in sorted(z.files, key=lambda k: int(k.split("_")[1]))]
r = [rot_half(p) for p in P]
poly = [(lambda c: (c, np.roll(c, -1, 0)))(p[np.argsort(np.mod(np.arange(len(p))*ri, 1.0))]) for p, ri in zip(P, r)]
pair = {f"{a}->{b}": 1e3*float(np.max(seg_dist(P[b], *poly[a]))) for a in range(4) for b in range(4) if a != b}
q = Fraction(float(np.mean(r))).limit_denominator(20)
out = dict(rotation=r, spread=max(r)-min(r), B_mm=max(pair.values()), pairs=pair, nearest_rational=str(q),
           distance_to_rational=float(np.mean(r))-q.numerator/q.denominator)
print(json.dumps(out, indent=1)); json.dump(out, open("posthoc2.json", "w"), indent=1)
