"""N20: trust-region Gauss-Newton/Broyden repair of selected401 on the native mirror.

Goals: W >= 0.005, FC <= 0.85, aspect = A0, iota/nfp >= iota0. Edge mirror monitored.
Starts from N19's FD Jacobian; one cold ns99 solve per iteration.
"""
import json, os, sys, time, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "n19"))
import fd
from metrics2 import metrics
fd.metrics = metrics
KEYS = ("vacuum_well", "flux_compression", "aspect", "iota_edge_per_fp")
SCALE = np.array([0.01, 0.1, 0.05, 0.001])

def residual(r, a0, i0):
    return np.array([min(r["vacuum_well"]-0.005, 0), max(r["flux_compression"]-0.85, 0),
                     r["aspect"]-a0, min(r["iota_edge_per_fp"]-i0, 0)])/SCALE

def main(step_json, secant_jsonl, out, iters=25, budget=1800, radius=0.01):
    t0 = time.time(); st = json.load(open(step_json))
    start = [((k, m, n), d) for (k, m, n), d in zip(st["modes"], st["dx"])]
    rows = [json.loads(l) for l in open(secant_jsonl)]
    s0 = next(r for r in rows if r.get("tag") == "start")
    fdr = [r for r in rows if r.get("mode") and r["h"] == 5e-3 and "error" not in r]
    modes = [tuple(r["mode"]) for r in fdr]
    J = np.array([[(r[k]-s0[k])/r["h"] for r in fdr] for k in KEYS])/SCALE[:, None]
    x = np.zeros(len(modes)); fd.OUT = out
    def run(x, tag):
        return fd.solve(start + [((k, m, n), float(v)) for (k, m, n), v in zip(modes, x) if v], tag)
    cur = run(x, "it0"); a0, i0 = cur["aspect"], cur["iota_edge_per_fp"]
    res = residual(cur, a0, i0); log = open(out, "a")
    log.write(json.dumps(dict(it=0, **cur, merit=float(res@res)))+"\n"); log.flush()
    for it in range(1, iters+1):
        if time.time()-t0 > budget or not res.any(): break
        dx = -np.linalg.pinv(J) @ res
        if np.linalg.norm(dx) > radius: dx *= radius/np.linalg.norm(dx)
        new = run(x+dx, f"it{it}")
        if "error" in new or new.get("ier", 1) != 0:
            radius /= 2; log.write(json.dumps(dict(it=it, rejected="solve", radius=radius, **new))+"\n"); continue
        nres = residual(new, a0, i0)
        raw = np.array([new[k]-cur[k] for k in KEYS])/SCALE
        J += np.outer(raw - J@dx, dx)/(dx@dx)  # Broyden on raw quantities
        ok = bool(nres@nres < res@res)
        if ok: x, cur, res, radius = x+dx, new, nres, radius*1.5
        else: radius /= 2
        log.write(json.dumps(dict(it=it, accepted=ok, radius=radius, step=float(np.linalg.norm(dx)),
                                  merit=float(nres@nres), **new))+"\n"); log.flush()
    json.dump(dict(start=st["dx"], start_modes=st["modes"], modes=modes, x=x.tolist(), final=cur), open(out.replace(".jsonl", "-x.json"), "w"))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
