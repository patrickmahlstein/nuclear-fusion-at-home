"""N29 (#48): narrow-domain bounce-action diagnostic from realized-flux-matched launches, reference401 fit.
Usage: python matched_bounce.py SNAPSHOT WOUT OUT.json  (repository root, one thread)"""
import importlib.util, json, math, sys, time
import numpy as np
sys.path.insert(0, "src")
from fusion_baselines import coil_bounce as bounce
from fusion_baselines.vmec_trace import trace_geometry
spec = importlib.util.spec_from_file_location("m28", sys.argv[4] if len(sys.argv) > 4 else "matched.py")
SNAP, WOUT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; NALPHA = int(sys.argv[5]) if len(sys.argv) > 5 else 16
sys.argv = [sys.argv[0], SNAP, WOUT, "/dev/null"]  # reuse N28 helpers without running its main body
src = open(spec.origin).read().split("cases = [(s, th)")[0]
g = {}; exec(compile(src, spec.origin, "exec"), g)
rz, labels_at, field, target = g["rz"], None, g["field"], g["target"]
trace, flux_of, axis, flux_edge = g["trace"], g["flux_of"], g["axis"], g["flux_edge"]
t0 = time.monotonic()

def s_real(points):
    out = [flux_of(p, axis) for p in trace(points, 60, 1e-10)]
    return [f/flux_edge for f, _ in out], [st for _, st in out]

class Shifted:  # target stand-in whose rz() launches at matched labels per alpha line
    def __init__(self, sig): self.sig = sig
    def rz(self, s, theta, phi):
        pts = [rz(sg, th) for sg, th in zip(self.sig, np.atleast_1d(theta))]
        return np.array([p[0] for p in pts]), np.array([p[1] for p in pts])

res = dict(surfaces=[])
for s in (0.25, 0.5, 0.75):
    ideal = trace_geometry(WOUT, s, 801, NALPHA, 2); th = ideal["theta"][0]
    sig = np.full(len(th), s); hist = []
    sr, st = s_real([rz(x, t) for x, t in zip(sig, th)]); hist.append(dict(sigma=sig.tolist(), s_real=sr))
    psig, psr = sig.copy(), np.array(sr); sig = sig + (s - psr)
    for it in range(4):
        sr, st = s_real([rz(x, t) for x, t in zip(sig, th)]); sr = np.array(sr); hist.append(dict(sigma=sig.tolist(), s_real=sr.tolist()))
        if np.all(abs(sr - s) <= 1e-3): break
        d = sr - psr; step = np.where(abs(d) > 1e-12, (sig - psig)/np.where(abs(d) > 1e-12, d, 1), 1.0)
        psig, psr, sig = sig.copy(), sr, np.clip(sig + (s - sr)*step, 1e-3, 0.999)
    matched = abs(np.array(sr) - s) <= 1e-3
    row = dict(s=s, matched=matched.tolist(), sigma=sig.tolist(), s_real=list(map(float, sr)), star=st, iterations=hist,
               ideal=bounce.measure(ideal))
    row["coil_target_launch"] = bounce.measure(bounce.trace_coils(field, target, s, ideal))
    row["coil_matched_launch"] = bounce.measure(bounce.trace_coils(field, Shifted(sig), s, ideal)) if matched.all() else \
        dict(error="unmatched alpha lines; matched diagnostic not computed", unmatched=int((~matched).sum()))
    res["surfaces"].append(row)
    print(s, "matched", int(matched.sum()), "/", len(matched), flush=True)

def narrow(key):
    cells = [c for r in res["surfaces"] for c in r[key].get("cells", []) if c["q"] in (0.1, 0.3, 0.5, 0.7, 0.9)]
    return float(np.mean([c["score"] for c in cells])) if len(cells) == 15 else None, len(cells)
for k in ("ideal", "coil_target_launch", "coil_matched_launch"):
    res[k + "_narrow"] = narrow(k)
res["seconds"] = time.monotonic() - t0
json.dump(res, open(OUT, "w"), indent=1, default=float)
print({k: res[k + "_narrow"] for k in ("ideal", "coil_target_launch", "coil_matched_launch")}, round(res["seconds"]))
